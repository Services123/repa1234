#! /usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater,CallbackQueryHandler,RegexHandler,ConversationHandler
import telegram
import os,sys
import requests, json
import datetime
import pymongo


TOKEN = "863685329:AAE28MbIM9GEu60v_J-z3zLu7wUqjcJZZeg"
PORT = int(os.environ.get('PORT', '43760'))

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0-97nom.mongodb.net/test?retryWrites=true")
db = client.get_database('shopbiz123')

kb = [[telegram.KeyboardButton('Наличие 💊'),telegram.KeyboardButton('Проверить оплату ✅')],
	[telegram.KeyboardButton('Инструкция 📄'),telegram.KeyboardButton('Оператор 📱')]]

kbMainMarkup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)

def orderForm1(bot, update,user_data):
	if  update.message.text ==u'🔙 Вернуться в меню':
		bot.send_message(chat_id=user.usr_id,text=
        'Вы вернулись в главное меню',
        reply_markup=kbMainMarkup)
		return ConversationHandler.END

	user_data['cost'] = update.message.text
	print('cost is '+update.message.text)
	kb_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True)
	update.effective_message.reply_text(
		        'Введите город', reply_markup=kb_markup)
	return 3

def orderForm2(bot, update,user_data):
	if  update.message.text ==u'🔙 Вернуться в меню':
		bot.send_message(chat_id=user.usr_id,text=
        'Вы вернулись в главное меню',
        reply_markup=kbMainMarkup)
		return ConversationHandler.END

	user_data['city'] = update.message.text
	print('city is '+update.message.text)
	kb_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True)
	update.effective_message.reply_text(
		        'Введите район', reply_markup=kb_markup)
	return 4

def orderForm3(bot, update,user_data):
	if  update.message.text ==u'🔙 Вернуться в меню':
		bot.send_message(chat_id=user.usr_id,text=
        'Вы вернулись в главное меню',
        reply_markup=kbMainMarkup)
		return ConversationHandler.END

	user_data['area'] = update.message.text
	print('area is '+update.message.text)
	kb_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True)
	update.effective_message.reply_text(
		        'Введите название (описание)', reply_markup=kb_markup)
	return 5

def orderForm4(bot, update,user_data):
	if  update.message.text ==u'🔙 Вернуться в меню':
		bot.send_message(chat_id=user.usr_id,text=
        'Вы вернулись в главное меню',
        reply_markup=kbMainMarkup)
		return ConversationHandler.END

	user_data['name'] = update.message.text
	print('name is '+update.message.text)
	kb_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True)
	update.effective_message.reply_text(
		        'Скиньте фотографию клада', reply_markup=kb_markup)
	return 6

def orderForm5(bot, update,user_data):
	print('asa')
	print('photo')
	if  update.message.text == u'🔙 Вернуться в меню':
		bot.send_message(chat_id=user.usr_id,text=
        'Вы вернулись в главное меню',
        reply_markup=kbMainMarkup)
		return ConversationHandler.END
	user_data['photochat'] = update.message.chat_id
	user_data['photoid'] = update.message.message_id

	insertOrder(user_data['cost'], user_data['city'], user_data['area'],user_data['name'],user_data['photochat'],user_data['photoid'])
	print('asa1')
	kb_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True)
	update.effective_message.reply_text(
		        'Товар добавлен!', reply_markup=kb_markup)
	return ConversationHandler.END


def SendDelOrder(bot,update):
	orders = db.orders.find({'status': True})
	for x in orders:
		bot.send_message(chat_id=update.message.chat_id, text=x['name']+'\n'+x['area'],
			reply_markup=telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(text='Удалить',callback_data=x['order_id']+'$$DEL')]]))

	bot.send_message(chat_id=update.message.chat_id, text = 'Доступные товары',reply_markup=telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True))

def getStat(bot,update):
	cost = 0
	for x in db.stat.find():
		cost = cost+int(x['cost'])
	clients = str(db.clients.count())

	bot.send_message(chat_id=update.message.chat_id, text = 'Всего продано товаров: '+str(db.stat.count())+'\n'+'Сумма проданных товаров: '+str(cost)+'\n'+'Всего людей в боте: '+clients+'\n',reply_markup=telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True))


def checkAdmin(bot,update,msg):
	if msg == u'1:Посмотреть статистику':
		getStat(bot,update)
	elif msg == u'2:Добавить клад':
		kb_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True)
		update.effective_message.reply_text(
		        'Введите цену, только цифры', reply_markup=kb_markup)
		return True
	elif msg == u'3:Удалить клады':
		SendDelOrder(bot,update)
	elif msg == u'4:Изменить админа':
		setAdmin(bot,update)
	elif msg == u'siJwBeApJKVj':
		changeAdmin(bot,update)
	return False


def setAdmin(bot,update):
	kb = [[telegram.KeyboardButton('1:Посмотреть статистику')],[telegram.KeyboardButton('2:Добавить клад')],
	[telegram.KeyboardButton('3:Удалить клады')],[telegram.KeyboardButton('4:Изменить админа')]]
	kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)

	bot.send_message(chat_id=update.message.chat_id,
					text="Напишите секретный код, если хотите стать админом",
					reply_markup=kb_markup)

	

def changeAdmin(bot,update):
	admin = db.clients.find_one({'admin':True})
	if admin != None:
		db.clients.update({'chat_id':admin['chat_id']}, {'chat_id': admin['chat_id'],'order_id':None,'admin':False}, upsert=True)

	chat_id = update.message.chat_id
	db.clients.update({'chat_id':chat_id}, {'chat_id': chat_id,'order_id':None,'admin':True}, upsert=True)
	kb = [[telegram.KeyboardButton('1:Посмотреть статистику')],[telegram.KeyboardButton('2:Добавить клад')],
	[telegram.KeyboardButton('3:Удалить клады')],[telegram.KeyboardButton('4:Изменить админа')]]
	kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
	bot.send_message(chat_id=update.message.chat_id,
					text="Выберите пункт админ-панели:",
					reply_markup=kb_markup)

def admin(bot,update):
	print('adminPanel...')
	kb = [[telegram.KeyboardButton('1:Посмотреть статистику')],[telegram.KeyboardButton('2:Добавить клад')],
	[telegram.KeyboardButton('3:Удалить клады')],[telegram.KeyboardButton('4:Изменить админа')]]
	kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
	print(update.message.text)
	utm=update.message.text.split(' ')
	if len(utm)>1:
		if utm[1] == '1@So4Zzcn^oQ':
			bot.send_message(chat_id=update.message.chat_id,
					text="Выберите пункт админ-панели:",
					reply_markup=kb_markup)


def updateClients(chat_id):
	db.clients.update({'chat_id':chat_id}, {'chat_id': chat_id,'order_id':None}, upsert=True)



def callback_alarm(bot, job):
	order_id = getClientOrder(job.context.message.chat_id)
	db.orders.update({'order_id':order_id}, { "$set": { 'status' : True  } } )
	db.clients.update({'chat_id':job.context.message.chat_id}, {'chat_id': job.context.message.chat_id,'order_id':None})
	bot.send_message(chat_id=job.context.message.chat_id, text='Ваша бронь на клад снята!',reply_markup=kbMainMarkup)


def updateClientOrder(chat_id, order_id, job,update):
	print('updatingStatus')
	db.orders.update({'order_id':order_id}, { "$set": { 'status' : False  } } )
	job.run_once(callback_alarm, 43200, context=update) 
	db.clients.update({'chat_id':chat_id}, {'chat_id': chat_id,'order_id':order_id}, upsert=True)

def getClientOrder(chat_id):
	client = db.clients.find_one({'chat_id':int(chat_id)})
	if client == None:
		return None
	return client['order_id']

def getOrderCost(order_id):
	order = db.orders.find_one({'order_id':order_id})
	return order['cost']

def insertOrder(cost, city, area,name,photochat,photoid):
	print('Inserting Oreder')
	order_id = str(datetime.datetime.now())
	db.orders.insert_one({'order_id': order_id,'cost':cost,
			'city':city,'area':area,'name':name,'status': True,'photochat':photochat,'photoid':photoid})

def sendOrderPhoto(bot,order_id,chat_id):

	kb_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True)
	order = db.orders.find_one({'order_id':order_id})
	try:
		bot.forward_message(chat_id=chat_id, from_chat_id=order['photochat'], message_id=order['photoid'])
		bot.send_message(chat_id=chat_id,text=u'Ваш клад доставлен!',reply_markup=kb_markup)
	except Exception as e:
		print(e)
		bot.send_message(chat_id=chat_id,text=u'Мы присоним свои извинения, на сервере произошла ошибка, напишите @nick свой номер заказа и вы обязательно найдете свой клад!',reply_markup=kb_markup)
	db.clients.update({'chat_id':chat_id}, { "$set": { 'order_id' : None  } } )
	db.stat.insert_one({'cost': order['cost']})
	db.orders.remove({'order_id':order_id})


def start(bot,update):
	updateClients(update.message.chat_id)
	kb = [[telegram.KeyboardButton('Наличие 💊'),telegram.KeyboardButton('Проверить оплату ✅')],
	[telegram.KeyboardButton('Инструкция 📄'),telegram.KeyboardButton('Оператор 📱')]]
	kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
	bot.send_message(chat_id=update.message.chat_id,
					text="Привет, у нас ты сможешь приобрести всё 🎁",
					reply_markup=kb_markup)

def mainMenu(bot, update):
	kb = [[telegram.KeyboardButton('Наличие 💊'),telegram.KeyboardButton('Проверить оплату ✅')],
	[telegram.KeyboardButton('Инструкция 📄'),telegram.KeyboardButton('Оператор 📱')]]
	kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
	bot.send_message(chat_id=update.message.chat_id,
					text="Выбери пункт меню 👇",
					reply_markup=kb_markup)

def sendingManual(bot,update):
	kb = [[telegram.KeyboardButton('Наличие 💊'),telegram.KeyboardButton('Проверить оплату ✅')],
	[telegram.KeyboardButton('Инструкция 📄'),telegram.KeyboardButton('Оператор 📱')]]
	kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
	bot.send_message(chat_id=update.message.chat_id,
					text="👇 Что тебе нужно сделать: \n💊 Выбрать товар в разделе \"Наличие\"\n💸 Пополнить кошелек на нужную сумму"+
					"\n🔢 В пункте \"Проверить оплату\" ввести номер транзации\n🎁 Найти свой клад",
					reply_markup=kb_markup)

def sendingOperator(bot,update):
	kb = [[telegram.KeyboardButton('Наличие 💊'),telegram.KeyboardButton('Проверить оплату ✅')],
	[telegram.KeyboardButton('Инструкция 📄'),telegram.KeyboardButton('Оператор 📱')]]
	kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
	bot.send_message(chat_id=update.message.chat_id,
					text="Если возникли вопросы - @nick",
					reply_markup=kb_markup)


def handleMessage(bot, update):
	msg = update.message.text
	if msg == u'Инструкция 📄':
		sendingManual(bot,update)
	elif msg == u'Оператор 📱':
		sendingOperator(bot,update)
	elif msg == u'Проверить оплату ✅':
		cOrder = getClientOrder(update.message.chat_id)
		if cOrder != None:
			kb_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True)
			update.effective_message.reply_text(
		        'Введите номер транзакции, без никаких дополнительных символов', reply_markup=kb_markup)
			return 1
		else:
			bot.send_message(chat_id=update.message.chat_id,
					text="Сначала нужно что-то купить 😅")
	elif msg ==u'Наличие 💊':
		bot.send_message(chat_id=update.message.chat_id,
					text="🔸 Выберите город 👇",
					reply_markup=telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(text='🌆 Харьков',callback_data='KHCT')]]))
	elif msg == u'🔙 Вернуться в меню':
		mainMenu(bot, update)
	elif msg == u'1:Посмотреть статистику':
		getStat(bot,update)
	elif msg == u'2:Добавить клад':
		kb_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True)
		update.effective_message.reply_text(
		        'Введите цену, только цифры', reply_markup=kb_markup)
		return 2
	elif msg == u'3:Удалить клады':
		SendDelOrder(bot,update)
	elif msg == u'4:Изменить админа':
		setAdmin(bot,update)
	elif msg == u'siJwBeApJKVj':
		changeAdmin(bot,update)


def sendArea(bot,update):
	areas = db.orders.find()
	buts = None
	if len(list(db.orders.find())) == 0:
		bot.send_message(chat_id=update.message.chat_id,
					text="Кладов по вашему городу нет")
		mainMenu(bot,update)
		return

	for x in areas:
		if buts == None:
			buts = [[telegram.InlineKeyboardButton(text=x['area'],callback_data=x['area']+'$$AREA')]]
		else:
			buts.append([telegram.InlineKeyboardButton(text=x['area'],callback_data=x['area']+'$$AREA')])

	bot.send_message(chat_id=update.message.chat_id,
					text="🔸 Выберите регион 👇",
					reply_markup=telegram.InlineKeyboardMarkup(buts))

def checkingAreas(bot,update,area):
	print('checkingAreas')
	kb_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True)
	bot.send_message(chat_id=update.message.chat_id,
					text=u"Вы выбрали: "+area, reply_markup=kb_markup)


	areas = db.orders.find({'area': area})

	if len(list(areas)) != 0:
		for x in db.orders.find({'area': area}):
			if x['status']:
				try:
					bot.send_message(chat_id=update.message.chat_id,
							text=x['name']+u'\nЦена: '+str(x['cost']),
							reply_markup=telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(text='Купить',callback_data=x['order_id']+'$$ORDER')]]))
				except Exception as e:
					print(e)

def checkingOrders(bot,chat_id, order,job_queue,update):
	print('checkingOrders')
	kb_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('Проверить оплату ✅')],
		[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True)
	orders = db.orders.find()
	if len(list(orders)) != 0:
		for x in db.orders.find():
			print('Debug 1')
			if x['order_id'] == order:
				print('Order 1')
				try:
					updateClientOrder(chat_id, order,job_queue,update)
				except Exception as e:
					print(e)
				try:
					bot.send_message(chat_id=chat_id,
							text=u"💸 Оплатите заказ на сумму "+str(getOrderCost(order))+u' на кошелек XXX. Через 12 часов бронь на заказ пропадет.',
							reply_markup=kb_markup)
				except Exception as e:
					print(e)
				break


def callbackQueryHandler(bot, update,job_queue):
	kb_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True)
	cqd = update.callback_query.data
	s = cqd.split('$$')
	if len(s)>1:
		if s[1] == 'YES':
			print('YES')
			sendOrderPhoto(bot,getClientOrder(s[0]),s[0])
		elif s[1] == 'NOT':
			bot.send_message(chat_id=s[0],text='Транзакция не была подтверждена, напишите оператору, если считаете, что произошла ошибка',reply_markup=kb_markup)
		elif s[1] == 'DEL':
			db.orders.remove({'order_id':s[0]})
			bot.send_message(chat_id=update.callback_query.message.chat_id,text = 'Товар был удален',reply_markup=kb_markup)
		elif s[1] == 'ORDER':
			checkingOrders(bot,update.callback_query.message.chat_id,s[0],job_queue,update.callback_query)
		elif s[1] == 'AREA':
			checkingAreas(bot,update.callback_query,s[0])

	if cqd == 'KHCT':
		sendArea(bot,update.callback_query)

	
	

def cancel(bot,update):
	return ConversationHandler.END

def chekingTransaction(bot,update,number):
	admin = db.clients.find_one({'admin':True})
	order_id = getClientOrder(update.message.chat_id)
	if order_id == None:
		return 
	cost = getOrderCost(order_id)
	
	bot.send_message(chat_id=admin['chat_id'],text=u'Вам приходил платеж '+ str(number)+u' на сумму '+str(cost),
		reply_markup=telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(text='Да',callback_data=str(update.message.chat_id)+'$$YES')],
			[telegram.InlineKeyboardButton(text='Нет',callback_data=str(update.message.chat_id)+'$$NOT')]]))


def checkingNumber(bot,update):
	kb = [[telegram.KeyboardButton('Наличие 💊'),telegram.KeyboardButton('Проверить оплату ✅')],
	[telegram.KeyboardButton('Инструкция 📄'),telegram.KeyboardButton('Оператор 📱')]]
	kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
	back_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('🔙 Вернуться в меню')]], resize_keyboard=True)
	msg = update.message.text
	if msg == u'🔙 Вернуться в меню':
		update.effective_message.reply_text(
	        'Выбери пункт меню 👇', reply_markup=kb_markup)
		return ConversationHandler.END
	elif msg.isdigit():
		update.effective_message.reply_text(
	        'Ожидайте подтверждения транзакции. ✅ Время ожидания от 5 до 20 минут!', reply_markup=back_markup)
		chekingTransaction(bot,update,msg)
	else:
		update.effective_message.reply_text(
	        'Вы ввели что-то не так, введите номер транзакции, без никаких дополнительных символов 👇', reply_markup=back_markup)
		return 1


conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, handleMessage)],

        states={
            1: [MessageHandler(Filters.text, checkingNumber)],

            2: [MessageHandler(Filters.text, orderForm1, pass_user_data=True)],
            3: [MessageHandler(Filters.text, orderForm2, pass_user_data=True)],
            4: [MessageHandler(Filters.text, orderForm3, pass_user_data=True)],
            5: [MessageHandler(Filters.text, orderForm4, pass_user_data=True)],
            6: [MessageHandler(Filters.photo, orderForm5, pass_user_data=True)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )


dispatcher.add_handler(conv_handler)


dispatcher.add_handler(CallbackQueryHandler(callbackQueryHandler,pass_job_queue=True))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('admin', admin))
dispatcher.add_handler(MessageHandler(Filters.text, handleMessage))

if __name__ == '__main__':
	#updater.start_polling()
	updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
	updater.bot.set_webhook("https://shopbizbot.herokuapp.com/" + TOKEN)
	updater.idle()
