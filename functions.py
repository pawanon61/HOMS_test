import datetime
import logging

# create  logger
level = logging.INFO
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers = [logging.FileHandler('HOMS_test.log'), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)
logger = logging.getLogger(__name__)

def get_user_confirmation():
	# ask user for confirmation. case insensitive; returns true if positive confirmation.
	answer = ""
	while answer not in ["y", "n"]:
		answer = input("This script moves real hardware. Do you want to continue(Y/N)?").lower()
	return answer == "y"

def verify_axes_coupled(object):
	logger.info("checking if %s axes are coupled" %object.name)
	if object.xgantry.decoupled.value == 1:
		logger.warning("xGantry status: decoupled")
	else:
		logger.info("yGantry status: coupled")

	if object.ygantry.decoupled.value == 1:
		logger.warning("ygantry status: decoupled")
	else:
		logger.info(" ygantry status: coupled")

def get_gantry_difference(object):
	logger.info("getting gantry differences for mirror %s" %object.name)
	logger.info("xgantry difference: %.4f" %object.xgantry.gantry_difference.value)
	logger.info("ygantry_difference: %.4f" %object.xgantry.gantry_difference.value)

def gantry_checks(object_method, how_much):
	logger.info("movement check....")
	initial_timestamp = object_method.readback.timestamp
	# request a move
	logger.info("moving by %f..." %how_much)
	object_method.umvr(how_much)
	# record final value
	logger.info("final gantry value for this axis: %.4f. Final gantry difference: %.4f. Time taken for move to complete: %.4f" %(object_method(), object_method.gantry_difference.value, object_method.readback.timestamp-initial_timestamp))
	# move in reverse direction
	logger.info("moving to original position...")
	object_method.umvr(-how_much)

def avg_noise_level(object):
	logger.info("recording 10 second pitch average value for %s ..." %object.name)
	position_values = []
	while len(position_values) <= 9:
		position_values.append(object.pitch.position)
		import time; time.sleep(1)
	average_noise_level = sum(position_values)/float(len(position_values))
	logger.info("%s: 10 second average noise level in mirror angle is %.4f %s" %(object.name, average_noise_level, object.pitch.egu))    

def rec_time_for_a_move(object, how_much):
	logger.info("for mirror %s, recording time for %f %s move ... " %(object.name, how_much, object.pitch.egu))
	initial_timestamp = object.pitch.readback.timestamp
	object.pitch.umvr(how_much)
	final_timestamp = object.pitch.readback.timestamp
	logger.info(final_timestamp - initial_timestamp)
	logger.info("moving in reverse direction to original position")
	object.pitch.umvr(-how_much)
	logger.info('done')  

def request_change_verify_axis(object_method, initial_position, initial_move_to, move_here_after_change_request):
	# object method corresponds to whichever axis you want to move
	logger.info("initial move...")
	object_method.mv(initial_move_to)
	while 1:
		# print("current position is %.9f" %object_method.position)
		if object_method.position > initial_move_to - 0.1 and object_method.position < initial_move_to + 0.1:
			object_method.stop()
			logger.info("stopped at %.4f" %object_method.position)
			break
	logger.info("issuing new move...")
	object_method.move(move_here_after_change_request)
	logger.info("final position is %.4f" %object_method.position) 
	if object_method() > move_here_after_change_request - 0.02 and object_method() < move_here_after_change_request + 0.02:
		logger.info("final position corresponds to changed target. success")
	else:
		logger.warning("final position doesnot match to changed target. failed: couldnot overwrite the command")
		
	# test high limit
	logger.info("going to high limit...")
	for ih in range(1,100000):
		object_method.mvr(1.0)
		if object_method.high_limit_switch.value == False:
			object_method.stop()
			logger.warning("you hit high limit switch at %s" %object_method.position)
			break
	# test low limit
	logger.info("going to low limit...")
	for il in range(1, 100000):
		object_method.mvr(-1.0)
		if object_method.low_limit_switch.value == False:
			object_method.stop()
			logger.warning("you hit low limit switch at %s" %object_method.position)
			break
	# 	restore to original position
	logger.info("restoring to original position")
	object_method.mv(initial_position)



