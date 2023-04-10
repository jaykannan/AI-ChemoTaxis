import random

from pygame import Vector2
import pygame
from enums import CProperty, FType
from logger import Logger
from monomer import Monomer
from globals import Globals
from partitionmanager import PartitionManager
from polymer import Polymer
from vesicle import Vesicle


class Environment:
    def __init__(self, num_objects, graphics_device, content, font):
        self.floating_objects = []
        self.partition_manager = PartitionManager(graphics_device)
        self.sf = font
        self.log_timer = 0.0
        self.game_timer = 0.0
        self.logger = []
        self.rand = random.Random()

        self.tex_vesicle = content.load("bubble")
        self.tex_monomer = content.load("monomer")

        # Initialize partitions 10x8 (change this if needed)
        self.partition_manager = PartitionManager(graphics_device)

        # Create 1% of them as vesicles, create log_data array to update every second
        for i in range(int(num_objects / 100)):
            vesicle = Vesicle(self.tex_vesicle)
            vesicle.v_radius = vesicle.v_radius_threshold = float(self.rand.randint(10, 25))
            vesicle.v_current_force = Vector2(0, self.rand.randint(10) - 5)
            vesicle.v_position = Vector2(self.rand.randint(graphics_device.viewport.width),
                                         self.rand.randint(graphics_device.viewport.height))
            vesicle.type = FType.VESICLE
            vesicle.ID = i
            self.floating_objects.append(vesicle)
            self.logger.append(Logger())

        # Create 99% of the objects as monomers
        for i in range(int((num_objects * 99) / 100)):
            monomer = Monomer(self.tex_monomer, self.random_enum(CProperty))
            monomer.v_position = Vector2(self.rand.randint(graphics_device.viewport.width),
                                         self.rand.randint(graphics_device.viewport.height))
            monomer.type = FType.MONOMER
            self.floating_objects.append(monomer)

    def random_enum(self, T):
        values = list(T)
        return values[self.rand.randint(0, len(values))]
    

    def update(floating_objects, partition_manager, logger, clock, eat_other_vesicles, eat_monomers, globals):
        elapsed_seconds = clock.tick() / 1000.0

        log_timer += elapsed_seconds
        game_timer += elapsed_seconds

        if log_timer > 1.0:  # log data every second
            for log in logger:
                log.updated = False

            for floating_object in filter(lambda fo: fo.type == FType.VESICLE, floating_objects):
                floating_object.log.radius = floating_object.vRadius
                floating_object.log.gameTime = game_timer
                logger[floating_object.ID].logs.append(floating_object.log)
                logger[floating_object.ID].updated = True

            log_timer -= 1.0

        # update normally
        for j in range(len(floating_objects)):
            floating_object = floating_objects[j]

            if floating_object.type == FType.VESICLE and floating_object.currentPartition >= 0:
                # check nearby objects
                for i in range(len(partition_manager.partitions[floating_object.currentPartition].object_list)):
                    target = floating_objects[partition_manager.partitions[floating_object.currentPartition].object_list[i]]

                    # call eatOtherVesicles to perform the eating function
                    eat_other_vesicles(game_time, j, floating_object, i, target)
                    # eat monomers only if it can grow that much
                    eat_monomers(j, floating_object, i, target)

                # model a stochastic mechanical event which causes a break in the vesicle larger than 50
                if (random.random()) < globals.MECHANICAL_EVENT and floating_object.vRadius > random.randint(50, 75):
                    # create new baby vesicles
                    baby_vesicle = Vesicle(floating_object.v_texture)
                    baby_vesicle.polymers.append(Polymer())
                    f_radius = 0.0

                    for i in range(len(floating_object.polymers[0].chain)):
                        f_radius += 1.0
                        if floating_object.polymers[0].chain[i].property == CProperty.SPLIT:
                            baby_vesicle.polymers[0].chain.append(floating_object.polymers[0].chain[i])

                            baby_vesicle.v_position = floating_object.v_position
                            baby_vesicle.v_mechanical_force = pygame.Vector2(random.randint(20) - 10, random.randint(20) - 10)
                            baby_vesicle.v_radius = baby_vesicle.v_radius_threshold = f_radius
                            f_radius = 0.0
                            baby_vesicle.type = FType.VESICLE

                            baby_vesicle.log.life_timer = floating_object.log.life_timer
                            baby_vesicle.log.distance_travelled = floating_object.log.distance_travelled
                            floating_object.log.life_timer = 0.0
                            baby_vesicle.log.number_of_monomers_eaten = floating_object.log.number_of_monomers_eaten
                            baby_vesicle.log.volume_growth = floating_object.log.volume_growth
                            baby_vesicle.ID = floating_object.ID

                            floating_objects.append(baby_vesicle)
                            baby_vesicle = Vesicle(floating_object.v_texture)
                            baby_vesicle.polymers.append(Polymer())

                        else:
                            floating_object.polymers[0].chain[i].offset = pygame.Vector2(
                                random.randint(int(f_radius)) - f_radius / 2,
                                random.randint(int(f_radius)) - f_radius / 2)

                            baby_vesicle.polymers[0].chain.append(floating_object.polymers[0].chain[i])

                        # destroy mother vesicle
                        floating_object.type = FType.ABSORBED

                # update polymer
                floating_object.update(elapsed_seconds)

        # remove monomers already absorbed
        floating_objects = [obj for obj in floating_objects if obj.type != FType.ABSORBED]

        # create new locations
        for partition in partition_manager.partitions:
            partition.object_list.clear()

        # add appropriate objects into partitions
        for i, floating_object in enumerate(floating_objects):
            floating_object.current_partition = partition_manager.get_partition_id(
                floating_object.v_position[0], floating_object.v_position[1])
            
            if 0 <= floating_object.current_partition < len(partition_manager.partitions):
                partition_manager.partitions[floating_object.current_partition].object_list.append(i)


        def eat_monomers(j, vesicle, i, target):
            if vesicle.v_radius >= vesicle.v_radius_threshold:
                return
            if target.type != FType.MONOMER or j == partition_manager.partitions[vesicle.current_partition].object_list[i]:
                return
            if not (Vector2.distance(vesicle.v_position, target.v_position) < vesicle.v_radius):
                return

            m = target  # assuming target is of Monomer type
            m.offset = Vector2(
                (random.randint(0, int(vesicle.v_radius * Globals.GROWTH_FACTOR)) -
                int(vesicle.v_radius * Globals.GROWTH_FACTOR / 2)),
                random.randint(0, int(vesicle.v_radius * Globals.GROWTH_FACTOR))
                - int(vesicle.v_radius * Globals.GROWTH_FACTOR / 2))

            # add monomer to chain 0 - it should divide itself later
            vesicle.polymers[0].chain.append(m)
            vesicle.v_radius += Globals.GROWTH_PER_MONOMER
            vesicle.log.number_of_monomers_eaten += 1

            # schedule for deletion
            target.type = FType.ABSORBED

            # pick only one object per frame per vesicle
            return
    
        def eat_other_vesicles(game_time, j, f, i, target):
            if target.type != FType.VESICLE or j == partition_manager.partitions[f.current_partition].object_list[i]:
                return
            if not (f.v_radius > target.v_radius):
                return
            if not (Vector2.distance(f.v_position, target.v_position) < f.v_radius):
                return

            f.v_radius_threshold += game_time.elapsed_game_time.total_seconds * Globals.ABSORB_RATE
            f.log.volume_growth += game_time.elapsed_game_time.total_seconds * Globals.ABSORB_RATE
            f.color = (255, 255, 255)
            target.v_radius -= game_time.elapsed_game_time.total_seconds * Globals.ABSORB_RATE
            target.v_radius_threshold = target.v_radius
            target.color = (0, 255, 0)

            if target.v_radius < target.v_radius_threshold:
                n = random.randint(Globals.MONOMER_MOVE_RATE)
                if len(target.polymers[0].chain) > n:
                    for count in range(n):
                        f.polymers[0].chain.append(target.polymers[0].chain[0])
                        target.polymers[0].chain.pop(0)
                        f.log.number_of_monomers_eaten += 1
                    target.v_radius_threshold = target.v_radius

            if target.v_radius < 1.0:
                target.type = FType.ABSORBED

        def draw(screen):
            for f in floating_objects:
                f.draw(screen)

                    



        
