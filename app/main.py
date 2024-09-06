# Write me a rock paper scissors game
# It must be written in Python3
# It must be a console application
# It must be a 2 player game
# It must be a best of 3 game
# It must be a random computer opponent


import random

import random
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
import os
import random
from bson import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    player_choice = request.json['choice']
    computer_choice = random.choice(['rock', 'paper', 'scissors'])
    result = determine_winner(player_choice, computer_choice)
    
    game_result = {
        'player_choice': player_choice,
        'computer_choice': computer_choice,
        'result': result
    }
    inserted_id = mongo.db.results.insert_one(game_result).inserted_id
    game_result['_id'] = str(inserted_id)
    
    return jsonify(game_result)

def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return 'It\'s a tie!'
    elif (player_choice == 'rock' and computer_choice == 'scissors') or \
         (player_choice == 'paper' and computer_choice == 'rock') or \
         (player_choice == 'scissors' and computer_choice == 'paper'):
        return 'You win!'
    else:
        return 'Computer wins!'

if __name__ == '__main__':
    app.run(debug=True)

