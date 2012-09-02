package ;

import flash.display.Shape;
import flash.display.StageAlign;
import flash.display.StageScaleMode;
import flash.Lib;
import flash.Vector;
import flash.Vector;

/**
 * ...
 * @author Josh Eklund
 */

class Vector
{
	public var angle : Float;
	public var length : Float;
	
	public function new(angle, length)
	{
		this.angle = angle;
		this.length = length;
	}
	
	public function add(vector2 : Vector)
	{
		var x = Math.sin(angle) * length + Math.sin(vector2.angle) * vector2.length;
		var y = Math.cos(angle) * length + Math.cos(vector2.angle) * vector2.length;
		length = Math.sqrt(x * x + y * y);
		angle = 0.5 * Math.PI - Math.atan2(y, x);
	}
	
    
}

class Main 
{
	
    static var myRectangle : flash.display.Shape;
    static var rectangleWidth = 50;
    static var rectangleHeight = 50;
   
    static var moveX : Float = 0; // the movement per frame of the rectangle on the horizontal axis
    static var moveY : Float = 0; // the movement per frame of the rectangle on the vertical axis
	
	static var gravity : Float = 0.3;
	
	static var player : Ghost;
	

    static function main()
    {
		player = new Ghost();
        myRectangle  = new flash.display.Shape();
        myRectangle.graphics.beginFill ( 0x990000 );
        myRectangle.graphics.lineStyle ( 1, 0x000000, 1, false, flash.display.LineScaleMode.NONE );
        myRectangle.graphics.drawRect ( 0, 0, rectangleWidth, rectangleHeight);
        myRectangle.graphics.endFill ();

        flash.Lib.current.addChild(player.box);

        flash.Lib.current.addEventListener(flash.events.Event.ENTER_FRAME,function(_) Main.onEnterFrame());
       
        flash.Lib.current.stage.addEventListener(flash.events.KeyboardEvent.KEY_DOWN, key_down);
        flash.Lib.current.stage.addEventListener(flash.events.KeyboardEvent.KEY_UP, key_up);
    }
   
    static function key_down(event:flash.events.KeyboardEvent)
    {
        if (event.keyCode == 37) // left arrow
            player.velocity.add(new Vector(3 * Math.PI / 2, 1));
        else if (event.keyCode == 39) // right arrow
            player.velocity.add(new Vector(Math.PI / 2, 1));
        else if (event.keyCode == 38) // up arrow
            player.velocity.add(new Vector(0, 1));
        else if (event.keyCode == 40) // down arrow
            player.velocity.add(new Vector(Math.PI, 1));
    }
   
    static function key_up(event:flash.events.KeyboardEvent)
    {
		/*
        if (event.keyCode == 37 && moveX == -1) // left arrow
            moveX = 0;
        else if (event.keyCode == 39 && moveX == 1) // right arrow
            moveX = 0;
        else if (event.keyCode == 38 && moveY == -1) // up arrow
            moveY = 0;
        else if (event.keyCode == 40 && moveY == 1) // down arrow
            moveY = 0;
			*/
    }

    static function onEnterFrame()
    {
		player.move();
		player.draw();
        // here we prevent the rectangle to move out of the display area
        if ( myRectangle.x > flash.Lib.current.stage.stageWidth - rectangleWidth -1)
		{
            myRectangle.x = flash.Lib.current.stage.stageWidth - rectangleWidth -1;
			moveX = - moveX; //Bounce
		}
        else if ( myRectangle.x <    0 )
		{
            myRectangle.x = 0;
			moveX = -moveX; //Bounce
		}
        if ( myRectangle.y > flash.Lib.current.stage.stageHeight - rectangleHeight -1)
		{
            myRectangle.y = flash.Lib.current.stage.stageHeight - rectangleHeight -1;
			moveY = -moveY;
		}
        else if ( myRectangle.y <    0 )
		{
            myRectangle.y = 0;
			moveY = -moveY;
		}
    }
}

class Ghost
{
	public var velocity: Vector;
	var x: Float;
	var y: Float;
	var width: Int;
	var height: Int;
	public var box: Shape;
	
	public function new()
	{
		velocity = new Vector(0, 0);
		x = 0;
		y = 0;
		width = 50;
		height = 50;
        box  = new flash.display.Shape();
	}
	public function draw()
	{
        box.graphics.beginFill ( 0x990000 );
        box.graphics.lineStyle ( 1, 0x000000, 1, false, flash.display.LineScaleMode.NONE );
        box.graphics.drawRect ( x, y, width, height);
        box.graphics.endFill ();
	}
    public function move()
	{
        x += Math.sin(velocity.angle) * velocity.length;
        y -= Math.cos(velocity.angle) * velocity.length;
		box.graphics.drawRect(x, y, width, height);
        /*bounce off walls
        if (x < width / 2 || x > self.cave.width - self.width / 2)
            self.angle = -self.angle
        if self.y < self.height / 2 or self.y > self.cave.height - self.height / 2:
            self.angle = math.pi - self.angle
		*/
	}
}
