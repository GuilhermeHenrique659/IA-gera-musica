
from src.presenter.AbstractPresenter import AbstractPresenter
from flask import render_template, request

class MusicPresenter(AbstractPresenter):
    
    def send(self, music_name):
        return render_template('index.html', music_name=music_name)
    
    def payload(self):
        return request.form