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
	
	static var player : Ghost;
	

    static function main()
    {
		player = new Ghost();
		player.draw();

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
    }

    static function onEnterFrame()
    {
		player.move();
    }
}

class Ghost
{
	public var velocity: Vector;
	var x: Float;
	var y: Float;
	var width: Int;
	var height: Int;
	var color: Int;
	public var box: Shape;
	
	public function new()
	{
		velocity = new Vector(0, 0);
		x = 0;
		y = 0;
		width = 50;
		height = 50;
		color = 0x220099;
        box  = new flash.display.Shape();
	}
	public function draw()
	{
        box.graphics.beginFill ( color );
        box.graphics.lineStyle ( 1, 0x000000, 1, false, flash.display.LineScaleMode.NONE );
        box.graphics.drawRect ( x, y, width, height);
        box.graphics.endFill ();
	}
    public function move()
	{
        x += Math.sin(velocity.angle) * velocity.length;
        y -= Math.cos(velocity.angle) * velocity.length;
        //bounce off walls
        if (x < 0)
		{
			x = 0;
            velocity.angle = -velocity.angle;
		}
		if (x > Lib.current.stage.stageWidth - width - 1)
		{
			x = Lib.current.stage.stageWidth - width - 1;
			velocity.angle = - velocity.angle;
		}
        if (y < 0)
		{
			y = 0;
			velocity.angle = Math.PI - velocity.angle;
		}
		if (y > Lib.current.stage.stageHeight - height - 1)
		{
			y = Lib.current.stage.stageHeight - height - 1;
            velocity.angle = Math.PI - velocity.angle;
		}
			
		box.x = x;
		box.y = y;

	}
}

class Pest extends Ghost
{
	
	public override function draw()
	{
        box.graphics.beginFill ( 0x990000 );
        box.graphics.lineStyle ( 1, 0x000000, 1, false, flash.display.LineScaleMode.NONE );
        box.graphics.drawRect ( x, y, width, height);
        box.graphics.endFill ();
	}
}
