import ptbot
import os
from pytimeparse import parse
from dotenv import load_dotenv


def render_progressbar(
    total,
    iteration,
    prefix='',
    suffix='',
    length=30,
    fill='█',
    zfill='░',
):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, author_id, message_id, time):
    secs = (time - secs_left)
    respond = (
        "Осталось {} сек.\n".format(secs_left) +
        render_progressbar(time, secs)
    )
    bot.update_message(author_id, message_id, respond)


def notify_final(author_id, message):
    answer = "Время истекло"
    bot.send_message(author_id, answer)
    print("Мне написал пользователь ID:", author_id)
    print("Он спрашивал:", message)
    print("Я ответил:", answer)


def reply(chat_id, question):
    time = parse(question)
    message_id = bot.send_message(chat_id, 'Запускаю таймер')
    print('ID сообщения', message_id)
    bot.create_countdown(
        time,
        notify_progress,
        author_id=chat_id,
        message_id=message_id,
        time=time,
    )
    bot.create_timer(time+1, notify_final, author_id=chat_id, message=question)


if __name__ == '__main__':
    load_dotenv()

    TG_TOKEN = os.getenv('TG_TOKEN')
    TG_CHAT_ID = os.getenv('TG_CHAT_ID')

    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(reply)
    bot.run_bot()
