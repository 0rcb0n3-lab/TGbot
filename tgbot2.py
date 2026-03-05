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


def notify_progress(secs_left, author_id, message_id, time, bot):
    secs = (time - secs_left)
    respond = (
        "Осталось {} сек.\n".format(secs_left) +
        render_progressbar(time, secs)
    )
    bot.update_message(author_id, message_id, respond)


def notify_final(author_id, message, bot):
    answer = "Время истекло"
    bot.send_message(author_id, answer)


def reply(chat_id, question, bot):
    time = parse(question)
    message_id = bot.send_message(chat_id, 'Запускаю таймер')

    bot.create_countdown(
        time,
        notify_progress,
        author_id=chat_id,
        message_id=message_id,
        time=time,
        bot=bot,
    )
    bot.create_timer(
        time+1,
        notify_final,
        author_id=chat_id,
        message=question,
        bot=bot,
    )


def main():
    load_dotenv()

    tg_token = os.getenv('TG_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')

    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(reply, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
