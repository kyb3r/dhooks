import json
import requests
import time
import datetime

class Webhook:
	def __init__(self, url, **kwargs):

		"""
		Initialise a Webhook Embed Object
		"""

		self.url = url #if '/slack' in url else url + '/slack'
		self.msg = kwargs['msg'] if 'msg' in kwargs else None
		self.color = kwargs['color'] if 'color' in kwargs else 123123
		self.json = None
		self.title = None
		self.title_url = None
		self.author = None
		self.author_icon = None
		self.author_url = None
		self.desc = None
		self.fields = []
		self.image = None
		self.thumbnail = None
		self.footer = None
		self.footer_icon = None
		self.ts = None


	def add_field(self,**kwargs):
		'''Adds a field to `self.fields`'''
		name = kwargs['name'] if 'name' in kwargs else ''
		value = kwargs['value'] if 'value' in kwargs else ''
		inline = kwargs['inline'] if 'inline' in kwargs else True

		field = { 

		'name' : name,
		'value' : value,
		'inline' : inline

		}

		self.fields.append(field)

	def set_desc(self,desc):
		self.desc = desc

	def set_author(self, **kwargs):
		self.author = kwargs['name'] if 'name' in kwargs else None
		self.author_icon = kwargs['icon'] if 'icon' in kwargs else None

	def set_title(self, **kwargs):
		self.title = kwargs['title'] if 'title' in kwargs else None
		self.title_link = kwargs['url'] if 'url' in kwargs else None

	def set_thumbnail(self, url):
		self.thumbnail = url

	def set_image(self, url):
		self.image = url

	def set_footer(self,**kwargs):
		self.footer = kwargs['text'] if 'text' in kwargs else None
		self.footer_icon = kwargs['icon'] if 'icon' in kwargs else None
		ts = kwargs['ts'] if 'ts' in kwargs else None
		if ts == True:
			self.ts = str(datetime.datetime.utcfromtimestamp(time.time()))
		elif ts.isdigit():
			self.ts = str(datetime.datetime.utcfromtimestamp(ts))
		else:
			raise Exception('Must be a numerical value')

	def del_field(self, index):
		self.fields.pop(index)



	def format(self,*arg):
		'''
		Formats the data into a payload
		'''

		data = {}
		if self.msg is not None:
			data["content"] = self.msg

		data["embeds"] = []
		embed = {}

		if self.author is not None:
			if 'author' in embed:
				embed["author"]["name"] = self.author
			else:
				embed["author"] = {"name": self.author}

		if self.author_icon is not None:
			if 'author' in embed:
				embed["author"]["icon_url"] = self.author_icon
			else:
				embed["author"] = {"icon_url": self.author_icon}

		if self.author_url is not None:
			if 'author' in embed:
				embed["author"]["url"] = self.author_url
			else:
				embed["author"] = {"url": self.author_url}
				
		if self.color is not None: embed["color"] = self.color 
		if self.desc is not None: embed["description"] = self.desc 
		if self.title is not None: embed["title"] = self.title 
		if self.title_url is not None: embed["url"] = self.title_url 
		if self.image is not None: embed["image"] = {"url": self.image}
		if self.thumbnail is not None: embed["thumbnail"] = {"url": self.thumbnail}

		if self.footer is not None:
			if 'footer' in embed:
				embed["footer"]['text'] = self.footer
			else:
				embed["footer"] = {"text": self.footer}
		 
		if self.footer_icon is not None:
			if 'footer' in embed:
				embed['footer']['icon_url'] = self.footer_icon
			else:
				embed["footer"] = {"icon_url": self.footer_icon}

		if self.ts is not None: embed["timestamp"] = self.ts 

		if self.fields:
			embed["fields"] = []
			for field in self.fields:
				f = {}
				f["name"] = field['name']
				f["value"] = field['value']
				f["inline"] = field['inline'] 
				embed["fields"].append(f)
			data["embeds"].append(embed)


		self.json = json.dumps(data, indent=4)


	def post(self):
		"""
		Send the JSON formated object to the specified `self.url`.
		"""
		self.format()
		headers = {'Content-Type': 'application/json'}
		result = requests.post(self.url, data=self.json, headers=headers)
		if result.status_code == 400:
			print("Post Failed, Error 400")
		else:
			print("Payload delivered successfuly")
			print("Code : "+str(result.status_code))
			print("")
			time.sleep(2)







		


