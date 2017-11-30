import json
from pygame.math import Vector2
import unittest
from pong.constants import *
import pong.game as game
import pong.entities as entities
import pong.common as common
import pygame


def dumps(obj):
    """Dump obj as a JSON string using common.to_json as default encoder."""
    return json.dumps(obj, default=common.to_json)

# class PongJsonifyEntitiesTestCase(unittest.TestCase):
#     def setUp(self):
#         self.pong = game.Pong()
#
#
# class GameEntityJsonifyTestCase(unittest.TestCase):
#     def setUp(self):
#         self.ge = entities.GameEntity()
#
#     def test_json_encode(self):
#         pass

class ToJSONTestCase(unittest.TestCase):
    def setUp(self):
        self.location = Vector2(20, 30)
        self.ball = entities.Ball(self.location)
        self.rect = self.ball.get_rect()
        self.player = game.Player(1)

    def test_class_value_stored(self):
        j = dumps(self.location)
        d = json.loads(j)
        self.assertIn('__class__', d.keys())
        self.assertIn('__value__', d.keys())

    def test_dump_location_vector(self):
        j = dumps(self.location)

        d = json.loads(j)
        # self.assertEqual(d['__value__']['x'], self.location.x)
        # self.assertEqual(d['__value__']['y'], self.location.y)
        self.assertEqual(d['__class__'], 'Vector2')
        self.assertEqual(d['__value__'][0], self.location.x)
        self.assertEqual(d['__value__'][1], self.location.y)

        # self.assertEqual(d['__value__'], [(*self.location,)])   # Check if coordinates are the same

    def test_dump_rectangle(self):
        j = dumps(self.rect)
        d = json.loads(j)

        self.assertEqual(d['__class__'], 'Rect')
        self.assertEqual(len(d['__value__']), 4)
        self.assertEqual(pygame.Rect(*d['__value__']), self.rect)

    def test_dump_game_entity(self):
        """Dumping GameEntity objects only dumps the rect"""
        j = dumps(self.ball)
        d = json.loads(j)
        print('d:', d)
        self.assertEqual(d['__class__'], 'Ball')

        # The game entity's rect is stored in its value, and is also serialised.
        # eg. rect = pygame.Rect(d['__value__']['__value__'])
        self.assertEqual(d['__value__']['__class__'], 'Rect')
        self.assertEqual(len(d['__value__']['__value__']), 4)

    def test_dump_player(self):
        j = dumps(self.player)
        d = json.loads(j)

        self.assertIn('rect', d.keys())
        self.assertEqual(d['__class__'], 'Player')
        self.assertEqual(d['number'], self.player.number)
        self.assertEqual(d['score'], self.player.score)
        # self.assertEqual(d['rect'], self.player.get_rect())


class FromJsonTestCase(unittest.TestCase):
    def setUp(self):
        self.location = Vector2(20, 30)
        self.ball = entities.Ball(self.location)
        self.rect = self.ball.get_rect()
        self.player = game.Player(1)

        self.jlocation = dumps(self.location)
        self.jball = dumps(self.ball)
        self.jrect = dumps(self.rect)
        self.jplayer = dumps(self.player)

    def test_from_json_to_vector2(self):
        loc = json.loads(self.jlocation, object_hook=common.from_json)
        self.assertIsInstance(loc, Vector2)
        self.assertIsNotNone(loc)
        self.assertEqual(loc, self.location)
        print('          loc:', loc)
        print('self.location:', self.location)

    def test_from_json_to_rect(self):
        rect = json.loads(self.jrect, object_hook=common.from_json)
        self.assertEqual(rect, self.rect)

    def test_from_json_to_ball(self):
        ball = json.loads(self.jball, object_hook=common.from_json)
        self.assertIsInstance(ball, entities.Ball)
        self.assertEqual(ball.get_rect(), self.ball.get_rect())
        print('     ball rect:', ball.get_rect())
        print('self.ball rect:', self.ball.get_rect())

    def test_from_json_to_player(self):
        p = json.loads(self.jplayer, object_hook=common.from_json)
        self.assertIsInstance(p, game.Player)
        self.assertEqual(p.get_rect(), self.player.get_rect())
        self.assertEqual(p.score, self.player.score)
        self.assertEqual(p.number, self.player.number)


class PongJsonTestCase(unittest.TestCase):
    def setUp(self):
        self.pong = game.Pong()

    def test_to_json(self):
        j = json.dumps(self.pong, default=common.to_json, separators=(',', ':'))
        print(j)
        print(type(j))
        d = json.loads(j)
        self.assertIn('__class__', d.keys())
        self.assertIn('1', d.keys())
        self.assertIn('2', d.keys())
        self.assertIn('b', d.keys())
        self.assertIn('state', d.keys())

    def test_from_json(self):
        j = json.dumps(self.pong, default=common.to_json, separators=(',', ':'))
        pong = json.loads(j, object_hook=common.from_json)
        self.assertIsInstance(pong, game.Pong)

        # Ball and players are different from each other
        self.assertNotEqual(pong.player1, pong.player2)
        self.assertNotEqual(pong.player1, pong.ball)