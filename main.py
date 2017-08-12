import sys, asyncio, threading, concurrent.futures
import processes, glob, telegram, hotword

async def main(executor):
	glob.init()
	
	if len(sys.argv) >= 2:
		await glob.m(int(sys.argv[1]), 'Back and Running!')

	loop = asyncio.get_event_loop()
	tasks = [
		loop.run_in_executor(executor, processes.speechEngine, glob.speech),
		loop.run_in_executor(executor, processes.techWritingKeepAlive),
		loop.run_in_executor(executor, hotword.init),
		loop.create_task(processes.alarmCheck(glob.bot)),
		loop.create_task(glob.bot.message_loop({
			'chat': telegram.onMessage,
			'callback_query': telegram.onCallbackQuery,
			'inline_query': telegram.onInlineQuery,
			'chosen_inline_result': telegram.onInlineResult
		})),
		loop.create_task(processes.manual()),
	]
	print('Listening...')
	await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)


if __name__ == '__main__':
	executor = concurrent.futures.ThreadPoolExecutor(6)
	loop = asyncio.get_event_loop()

	try:
		loop.run_until_complete(main(executor))
	finally:
		glob.cleanup()
		loop.close()
		print('Goodbye!')
