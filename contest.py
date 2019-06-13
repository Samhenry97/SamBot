from datetime import datetime, timedelta, timezone
import requests, pytz

CF_BASE_URL = 'http://codeforces.com/'
CF_API_URL = CF_BASE_URL + 'api/'

def getUpcomingContests():
	response = requests.get(CF_API_URL + 'contest.list')
	data = response.json()
	if data['status'] != 'OK':
		return 'Error fetching contests.'
	upcoming = []
	for contest in data['result']:
		if contest['phase'] == 'BEFORE':
			upcoming.append(contest)
	upcoming.sort(key=lambda contest: -contest['relativeTimeSeconds'])
	upcoming = upcoming[:5]
	res = []
	for contest in upcoming:
		when = datetime.fromtimestamp(contest['startTimeSeconds'])
		until = timedelta(seconds=abs(contest['relativeTimeSeconds']))
		res.append('{}\n{}\n{} until start\n{} hours\n{}'.format(
				contest['name'], 
				when.strftime('%A, %B %d, %Y at %-I:%M:%S %p'),
				'{} days, {} hours, {} minutes'.format(until.days, until.seconds//3600, (until.seconds//60)%60),
				contest['durationSeconds'] / 60 / 60,
				'{}contest/{}'.format(CF_BASE_URL, contest['id'])
			)
		)
	message = 'Showing {} upcoming contests:\n\n'.format(len(res))
	return message + '\n\n'.join(res)
