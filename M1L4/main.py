from flask import Flask, render_template, session, redirect, url_for
from logic import Pokemon  # сохраняем класс Pokemon в отдельный файл
import random

import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # нужен для сессий

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/go')
def go():
    trainer_name = session.get('trainer_name')
    if not trainer_name:
        trainer_name = f"Trainer_{random.randint(1000, 9999)}"
        session['trainer_name'] = trainer_name

    if 'pokemon' not in session:
        pokemon = Pokemon(trainer_name)
        session['pokemon'] = {
            'name': pokemon.name,
            'img_url': pokemon.img,
            'info': pokemon.info()
        }
        return render_template(
            'pokemon.html',
            name=pokemon.name,
            img_url=pokemon.img,
            info=pokemon.info()
        )
    else:
        return "Ты уже создал себе покемона!"

@app.route('/level-up')
def level_up():
    """Маршрут для повышения уровня покемона"""
    if 'pokemon' in session:
        # Пересоздаём объект, чтобы применить изменения
        trainer_name = session['trainer_name']
        pokemon = Pokemon(trainer_name)
        result = pokemon.level_up()
        session['pokemon']['info'] = pokemon.info()  # обновляем информацию в сессии
        return render_template('pokemon.html', name=pokemon.name, img_url=pokemon.img, info=pokemon.info())
    else:
        return "Сначала создай покемона!"

if __name__ == '__main__':
    app.run(debug=True)