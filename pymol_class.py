import pymol
from pymol import cmd

class PymolRun:
    @staticmethod
    def main(queue):
        print('### LAUCH PYMOL')
        pymol.finish_launching()
        cmd.fetch('1d86')

        while True:
            # {'cmd': [0, 1, 3]}
            # If the queue is empty, queue.get() will block until the queue has data
            cmd_dict = queue.get()
            if cmd_dict.get('translate'):
                cmd.translate(cmd_dict['translate'])
            elif cmd_dict.get('rotate'):
                cmd.rotate('y', cmd_dict['rotate'])
            elif cmd_dict.get('save'):
                cmd.save(cmd_dict['save'])
            elif cmd_dict.get('rotate180right'):
                cmd.rotate("y", cmd_dict['rotate180right'])
            elif cmd_dict.get('rotate180left'):
                cmd.rotate("y", cmd_dict['rotate180left'])
            elif cmd_dict.get('rotateup'):
                cmd.rotate("x", cmd_dict['rotateup'])
            elif cmd_dict.get('rotatedown'):
                cmd.rotate("x", cmd_dict['rotatedown'])

