import sys, asyncio, threading, concurrent.futures, logging
import processes, glob, hotword, server, bots.messenger, bots.telegram


async def main(executor):
	glob.init()
	
	if len(sys.argv) >= 2 and sys.argv[1] != 'DEBUG':
		await glob.m(glob.db.getChatById(int(sys.argv[1])), 'Back and Running!')
	elif len(sys.argv) < 2 or sys.argv[1] != 'DEBUG':
		logging.basicConfig(level=logging.ERROR)
		logging.getLogger().setLevel(logging.ERROR)

	loop = asyncio.get_event_loop()
	tasks = [
		loop.run_in_executor(executor, processes.speechEngine, glob.speech),
		loop.run_in_executor(executor, processes.techWritingKeepAlive),
		loop.run_in_executor(executor, hotword.listen),
		loop.run_in_executor(executor, bots.messenger.listen),
		loop.run_in_executor(executor, server.listen),
		loop.create_task(bots.telegram.listen()),
		loop.create_task(processes.alarmCheck()),
		loop.create_task(processes.manual()),
	]
	print('Ready to Go!')
	await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)


if __name__ == '__main__':
	executor = concurrent.futures.ThreadPoolExecutor(8)
	loop = asyncio.get_event_loop()

	try:
		loop.run_until_complete(main(executor))
	finally:
		glob.cleanup()
		loop.close()
		print('Goodbye!')
