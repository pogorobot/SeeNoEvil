package ;

import flash.display.StageAlign;
import flash.display.StageScaleMode;
import flash.Lib;

/**
 * ...
 * @author Josh Eklund
 */

class Main 
{
	
    static var myRectangle : flash.display.Shape;
    static var rectangleWidth = 50;
    static var rectangleHeight = 50;
   
    static var moveX : Float = 0; // the movement per frame of the rectangle on the horizontal axis
    static var moveY : Float = 0; // the movement per frame of the rectangle on the vertical axis
	
	static var gravity : Float = 0.5;
	

    static function main()
    {
        myRectangle  = new flash.display.Shape();
        myRectangle.graphics.beginFill ( 0x990000 );
        myRectangle.graphics.lineStyle ( 1, 0x000000, 1, false, flash.display.LineScaleMode.NONE );
        myRectangle.graphics.drawRect ( 0, 0, rectangleWidth, rectangleHeight);
        myRectangle.graphics.endFill ();

        flash.Lib.current.addChild(myRectangle);

        flash.Lib.current.addEventListener(flash.events.Event.ENTER_FRAME,function(_) Main.onEnterFrame());
       
        flash.Lib.current.stage.addEventListener(flash.events.KeyboardEvent.KEY_DOWN, key_down);
        flash.Lib.current.stage.addEventListener(flash.events.KeyboardEvent.KEY_UP, key_up);
    }
   
    static function key_down(event:flash.events.KeyboardEvent)
    {
        if (event.keyCode == 37) // left arrow
            moveX -= 1;
        else if (event.keyCode == 39) // right arrow
            moveX += 1;
        else if (event.keyCode == 38) // up arrow
            moveY -= 1;
        else if (event.keyCode == 40) // down arrow
            moveY += 1;
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
        myRectangle.x += moveX;
        myRectangle.y += moveY;
		moveY += gravity; //fall
       
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