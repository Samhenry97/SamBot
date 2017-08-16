import sys, asyncio, threading, concurrent.futures
import processes, glob, telegram, hotword, facebook, telegram

async def main(executor):
	glob.init()
	
	if len(sys.argv) >= 2:
		try:
			await glob.m(glob.db.getChatById(int(sys.argv[1])), 'Back and Running!')
		except:
			pass

	loop = asyncio.get_event_loop()
	tasks = [
		loop.run_in_executor(executor, processes.speechEngine, glob.speech),
		loop.run_in_executor(executor, processes.techWritingKeepAlive),
		loop.run_in_executor(executor, hotword.listen),
		loop.run_in_executor(executor, facebook.listen),
		loop.create_task(processes.alarmCheck(telegram.bot)),
		loop.create_task(telegram.bot.message_loop({
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
	executor = concurrent.futures.ThreadPoolExecutor(7)
	loop = asyncio.get_event_loop()

	try:
		loop.run_until_complete(main(executor))
	finally:
		glob.cleanup()
		loop.close()
		print('Goodbye!')
