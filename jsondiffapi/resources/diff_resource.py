from flask_restful import Api, Resource
from flask import request
from flask import jsonify
from flask import current_app
from jsondiffapi.models.models import *
from jsondiff import diff
from jsondiff import Symbol
from bson.objectid import ObjectId
import base64
import json

class Diff(Resource):
    def get(self, id=None):
        current_app.logger.debug('GET id:%s', id)

        try:
            diffo = DiffReq.objects.get(diff_id=id)
        except DoesNotExist, e:
            current_app.logger.debug(e)
            return { "error": "Resourse does not exist" }, 404

        if diffo.left and diffo.right:
            dleft = json.loads(base64.b64decode(diffo.left))
            dright = json.loads(base64.b64decode(diffo.right))
        else:
            return { "error": "You need provide left and right objects" }, 400

        print len(dleft)
        print len(dright)

        if len(dleft) != len(dright):
            return {"result": "objects should have same size"}

        response = {}
        response["result"]={}
        result = diff(dleft, dright, syntax='explicit')

        if not result:
            return {"result": "objects have no difference"}
        else:
            for i in result:
                response["result"][str(i).replace("$", "")] = result[i]

        return jsonify(response)

class AddLeft(Resource):
    def post(self, id=None):
        current_app.logger.debug('POST id:%s', id)
        current_app.logger.debug('request.data: %s', request.data)
        try:
            decoded_data = base64.decodestring(request.data)
            current_app.logger.debug('decoded_data: %s', decoded_data)
        except Exception, e:
            current_app.logger.error(e)
            return { "error": "Invalid base64 string" }, 400

        try:
            json_object = json.loads(decoded_data)
            current_app.logger.debug('decoded data: %s', json_object)
        except ValueError, e:
            current_app.logger.error(e)
            return { "error": "This is not a valid Json object" }, 400

        #-----------

        try:
            diffo = DiffReq.objects.get(diff_id=id)
            diffo.left = request.data
        except DoesNotExist, e:
            diffo = DiffReq(left=request.data, diff_id=id)
            current_app.logger.debug("Object %s does not exists, saving a new one", id)
        diffo.save()

        return jsonify(diffo)

class AddRight(Resource):
    def post(self, id=None):
        current_app.logger.debug('POST id:%s', id)
        current_app.logger.debug('request.data: %s', request.data)
        try:
            decoded_data = base64.decodestring(request.data)
            current_app.logger.debug('decoded_data: %s', decoded_data)
        except Exception, e:
            current_app.logger.error(e)
            return { "error": "Invalid base64 string" }, 400

        try:
            json_object = json.loads(decoded_data)
            current_app.logger.debug('decoded data: %s', json_object)
        except ValueError, e:
            current_app.logger.error(e)
            return { "error": "This is not a valid Json object" }, 400

        #-----------

        try:
            diffo = DiffReq.objects.get(diff_id=id)
            diffo.right = request.data
        except DoesNotExist, e:
            diffo = DiffReq(right=request.data, diff_id=id)
            current_app.logger.debug("Object %s does not exists, saving a new one", id)
        diffo.save()

        return jsonify(diffo)
