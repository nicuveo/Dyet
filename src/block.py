# block.py
#
# This file sets up the blocks



########## Imports ##########

import math
import color

from tools.graph import Graph
from tools.image import Image
from tools import image_builder
from command import Commands
from color import Colors



########## Declarations ##########

# Block ABC

class Block:
    def __init__(self, command):
        self.color = None
        self.command = command

    def minimum_size(self):
        raise NotImplemented()

    def colorize(self, start_color):
        self.color = start_color
        if self.command:
            return color.command_next(start_color, self.command)
        return start_color

    def render(self, width, height):
        raise NotImplemented()


# Leaf block

class LeafBlock(Block):
    def __init__(self, command, size = 0):
        Block.__init__(self, command)
        self.size = size

    def minimum_size(self):
        return (1, max(1, self.size))

    def render(self, width, height):
        assert(width == 1)
        assert(height >= self.size)
        if self.size == 0:
            return Image(1, height, self.color.rgb())
        res = Image(1, height, Colors.RGB_B)
        for row in range(0, self.size):
            res.pixel_set(0, row, self.color.rgb())
        return res;


# Noop block

class NoopBlock(LeafBlock):
    def __init__(self):
        LeafBlock.__init__(self, Commands.NOOP)


# End block

class EndBlock(Block):
    def __init__(self):
        Block.__init__(self, None)
        self.color = None

    def minimum_size(self):
        return (4, 5)

    def render(self, width, height):
        rgb = self.color.rgb()
        res = Image(width, height, rgb)
        col1 = int(    height / 3)
        col2 = int(2 * height / 3)
        for col in range (0, height):
            if (col >= col2):
                res.pixel_set(0, col, Colors.RGB_B)
            res.pixel_set(1, col, Colors.RGB_B if col < col1 or col >= col2 else Colors.RGB_W)
            res.pixel_set(3, col, Colors.RGB_B)
        return res


# Block list

class BlockList(Block):
    def __init__(self):
        Block.__init__(self, None)
        self.blocks = []

    def minimum_size(self):
        if self.blocks:
            sizes = [block.minimum_size() for block in self.blocks]
            return (sum(size[0] for size in sizes),
                    max(size[1] for size in sizes))
        return (0, 0)

    def colorize(self, start_color):
        for block in self.blocks:
            start_color = block.colorize(start_color)
        return start_color

    def render(self, width, height):
        res = Image(max(width, 1), max(height, 1))
        col = 0
        for block in self.blocks:
            bsize = block.minimum_size()
            image_builder.paste_sub_image(res, block.render(bsize[0], height), col, 0)
            col += bsize[0]
        assert(col == width)
        return res


# If block

class IfBlock(Block):
    def __init__(self):
        Block.__init__(self, None)
        self.if_block = BlockList()
        self.else_block = BlockList()

    def minimum_size(self):
        ibs = self.if_block.minimum_size()
        ebs = self.else_block.minimum_size()
        return (5 + max(ibs[1], 3) + max(ebs[1], 3),
                8 + max(ibs[0], ebs[0]))

    def colorize(self, color):
        self.color = color
        self.if_block.colorize(color)
        self.else_block.colorize(color)
        return color

    def render(self, width, height):
        res = Image(width, height, Colors.RGB_B)
        ibs = self.if_block.minimum_size()
        ebs = self.else_block.minimum_size()
        ibw = max(ibs[1], 3)
        ebw = max(ebs[1], 3)
        ibh = ibs[0]
        ebh = ebs[0]
        ebb = 1
        ebe = ebb + ebw - 1
        ibb = ebe + 2
        ibe = ibb + ibw - 1
        assert(width == ibe + 4)

        pix_color = self.color
        res.pixel_set(0, 0, pix_color.rgb())
        pix_color = color.command_next(pix_color, Commands.DUPLICATE)
        res.pixel_set(1, 0, pix_color.rgb())
        pix_color = color.command_next(pix_color, Commands.NOT)
        res.pixel_set(2, 0, pix_color.rgb())
        pix_color = color.command_next(pix_color, Commands.POINTER)
        res.pixel_set(ebe   + 1,          0, Colors.RGB_W)
        res.pixel_set(ibe   + 1, height - 1, Colors.RGB_W)
        res.pixel_set(width - 1,          0, Colors.RGB_W)
        image_builder.draw_rect(res, (  3, 0), (ebe, 0), pix_color.rgb())
        image_builder.draw_rect(res, (ibb, 0), (ibe, 0), pix_color.rgb())
        image_builder.draw_rect(res, (ebb, 1), (ebe, 1), Colors.RGB_W)
        image_builder.draw_rect(res, (ibb, 1), (ibe, 1), Colors.RGB_W)
        image_builder.draw_rect(res, (ebb, ebh + 2), (ebe, height - 4), Colors.RGB_W)
        image_builder.draw_rect(res, (ibb, ibh + 2), (ibe, height - 4), Colors.RGB_W)
        image_builder.draw_rect(res, (ebb, height - 5), (ebe, height - 5), pix_color.rgb())
        image_builder.draw_rect(res, (ibb, height - 5), (ibe, height - 5), pix_color.rgb())
        pix_color = color.command_next(pix_color, Commands.PUSH)
        image_builder.draw_rect(res, (ebb, height - 4), (ebe, height - 4), pix_color.rgb())
        image_builder.draw_rect(res, (ibb, height - 4), (ibe, height - 4), pix_color.rgb())
        pix_color = color.command_next(pix_color, Commands.POP)
        image_builder.draw_rect(res, (ebe - 2, height - 3), (ebe, height - 3), pix_color.rgb())
        image_builder.draw_rect(res, (ibe - 2, height - 3), (ibe, height - 3), pix_color.rgb())
        pix_color = color.command_next(pix_color, Commands.PUSH)
        image_builder.draw_rect(res, (1, height - 2), (ibe, height - 1), pix_color.rgb())
        pix_color = color.command_next(pix_color, Commands.POINTER)
        image_builder.draw_rect(res, (1, height - 1), (ibe, height - 1), pix_color.rgb())
        image_builder.draw_rect(res, (width - 2, 0), (width - 2, height - 1), pix_color.rgb())

        image_builder.paste_sub_image(res, self.if_block.render(  ibh, ibw), ibb, 2, image_builder.PLUS_90)
        image_builder.paste_sub_image(res, self.else_block.render(ebh, ebw), ebb, 2, image_builder.PLUS_90)
        return res


# While block

class WhileBlock(Block):
    def __init__(self):
        Block.__init__(self, None)
        self.while_block = BlockList()

    def minimum_size(self):
        wbs = self.while_block.minimum_size()
        return (4 + wbs[1], 4 + wbs[0])

    def colorize(self, color):
        self.color = color
        self.while_block.colorize(color)
        return color

    def render(self, width, height):
        res = Image(width, height, Colors.RGB_B)
        wbs = self.while_block.minimum_size()
        pix_color = self.color
        res.pixel_set(0, 0, pix_color.rgb())
        res.pixel_set(1, 1, pix_color.rgb())
        res.pixel_set(1, height - 1, pix_color.rgb())
        res.pixel_set(2, height - 1, Colors.RGB_W)
        res.pixel_set(width - 1,  0, Colors.RGB_W)
        pix_color = color.command_next(pix_color, Commands.DUPLICATE)
        res.pixel_set(1, 0, pix_color.rgb())
        pix_color = color.command_next(pix_color, Commands.NOT)
        res.pixel_set(2, 0, pix_color.rgb())
        pix_color = color.command_next(pix_color, Commands.POINTER)
        image_builder.draw_rect(res, (3, 0), (width - 2, 0), pix_color.rgb())
        image_builder.draw_rect(res, (3, 1), (width - 2,  1), Colors.RGB_W)
        image_builder.draw_rect(res, (1, 2), (1, height - 2), Colors.RGB_W)
        image_builder.draw_rect(res, (3, wbs[0] + 2), (width - 2, height - 2), Colors.RGB_W)
        image_builder.draw_rect(res, (3, height - 1), (width - 2, height - 1), pix_color.rgb())
        image_builder.paste_sub_image(res, self.while_block.render(wbs[0], wbs[1]), 3, 2, image_builder.PLUS_90)
        return res
