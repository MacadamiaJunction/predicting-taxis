import numpy as np

# Taxi state
REST = 0
MOVE = 1

# Taxi command
GO = 0 # Must go to a location, no distractions
GO_SIM = 1 # Head towards to a location, allowed to pickup calls in between
TELEPORT = 2 # Teleport to a location

AVG_SPEED = 0.005  # Calculated from data
IDLE_INTERVAL = 60 * 30  # Half hour


class Taxi(object):

    def __init__(self, start_time, start_loc):
        """
        Initialization. All taxis start by resting at a location.
        """
        self.last_command_timestamp = start_time
        self.cur_loc = start_loc
        self.status = REST
        self.commands = [] # Command queue
        self.inactive = False

        # Stats
        self.total_distance = 0.0
        self.total_paid_distance = 0.0

    def schedule_go(self, pickup_time, pickup_loc, drop_time, drop_loc):
        """
        Add a GO command to taxi queue
        """
        self.commands.append((GO, pickup_time, pickup_loc,
            drop_time, drop_loc))
        self.inactive = False

    def schedule_go_sim(self, target_loc):
        """
        Add a GO_SIM command to taxi queue
        """
        self.commands.append((GO_SIM, self.last_command_timestamp,
            self.cur_loc, target_loc))
        self.inactive = False

    def advance_time(self, target_time):
        """
        Consumes tasks for this taxi in the queue.

        If taxi is going towards somewhere using GO_SIM, it checks if we
        have a GO command scheduled after GO_SIM and the time for that GO
        command has already come. In that case, taxi stops going with GO_SIM
        and moves towards the pickup request from its current position.

        If taxi is going with GO_SIM but there are no tasks, it will continue
        until it reaches its destination.

        Otherwise it just picks the passenger and delivers her to her
        destination.

        :param target_time: absolute time position for the simulation, has to be later than the previous value (cannot go backwards)
        """
        assert(target_time > self.last_command_timestamp)

        if len(self.commands) == 0 and target_time - self.last_command_timestamp > IDLE_INTERVAL:
            self.inactive = True  # Has not received a command for a long 
                                    # time, sleep.
            return

        while len(self.commands) > 0:
            cur_command = self.commands[0]
            param_tuple = cur_command[1::]

            if cur_command[0] == GO_SIM:
                scheduled_time, scheduled_loc, target_loc = param_tuple

                if len(self.commands) == 2 and self.commands[1][0] == GO and \
                    target_time - self.commands[1][1] >= 0:
                    # We have a GO command scheduled already after this one 
                    # and the pickup request was already made
                    # So "move" until we receive the order, then stop and move 
                    # towards the new order.
                    # We just teleport to the source, otherwise we need to get
                    # a separate queue that we need to check
                    # Unnecessary complexity
                    pickup_time, pickup_loc, _, _ = self.commands[1][1::]
                    new_loc = self.simulate_move(scheduled_time,
                        scheduled_loc, target_loc, pickup_time)

                    # Move from the previous location to location at the time  
                    # of pickup request and from there to the actual pickup
                    # location
                    # All unpaid
                    self.total_distance += euclidean_distance(self.cur_loc,
                        new_loc) + euclidean_distance(new_loc, pickup_loc)

                    # Teleport
                    self.cur_loc = pickup_loc

                    # Remove GO_SIM from queue
                    self.commands.pop(0)
                    self.last_command_timestamp = target_time
                else:
                    # We are going towards some cluster,
                    # noone is waiting for us
                    new_loc = self.simulate_move(scheduled_time,
                        scheduled_loc, target_loc, target_time)

                    # This is unpaid travel, so only add to total distance
                    distance_traveled = euclidean_distance(self.cur_loc,
                        new_loc)
                    self.total_distance += distance_traveled

                    self.cur_loc = new_loc

                    if self.cur_loc == target_loc:
                        # We already arrived at the location
                        self.commands.pop(0)  
                        self.last_command_timestamp = target_time
                    else:
                        break  # We are still going towards somewhere

            elif cur_command[0] == GO:
                # We are actually carrying someone
                _, pickup_loc, drop_time, drop_loc = param_tuple

                # Hacky, sort of teleportation
                if drop_time - self.last_command_timestamp > 0:
                    # Unpaid travel
                    self.total_distance += euclidean_distance(self.cur_loc, pickup_loc)

                    # We are getting paid for this
                    distance_traveled_with_customer = euclidean_distance(pickup_loc, drop_loc)
                    self.total_distance += distance_traveled_with_customer
                    self.total_paid_distance += distance_traveled_with_customer

                    self.cur_loc = drop_loc
                    self.commands.pop(0)
                    self.last_command_timestamp = target_time
                else:
                    break  # Still not arrived yet

    def simulate_move(self, start_time, start_loc, end_loc, cur_time):
        """
        Simulates a continuous movement towards a target location,
        following a line trajectory.

        :return: a tuple with updated x, y coordinates
        """
        elapsed = cur_time - start_time

        x_diff = (end_loc[0] - start_loc[0])
        y_diff = (end_loc[1] - start_loc[1])

        # TODO: Check please -- MM: seems correct
        angle = np.arctan(y_diff / y_diff)
        delta_x = np.cos(angle) * AVG_SPEED * elapsed
        delta_y = np.sin(angle) * AVG_SPEED * elapsed

        x_update = start_loc[0] + delta_x
        y_update = start_loc[1] + delta_y

        if x_update > x_diff or y_update > y_diff:  # Overshoot
            return end_loc[0], end_loc[1]
        else:
            return start_loc[0] + x_update, start_loc[1] + y_update


def euclidean_distance(loc1, loc2):
    """
    :loc1: Location in array-like of length 2  
    :loc2: Location in array-like of length 2
    """
    return np.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)
