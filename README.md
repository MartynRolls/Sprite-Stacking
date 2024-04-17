## Sprite Stacking with Python's Pygame

I came accross this short clip of a racing game, and was completely taken by the artwork. Somehow, in this 2d game, the enviorment appeared to be 3 dimensional.
This was achieved using a technique using sprite stacking, layering many 2d images on top of one another to simulate a 3d image.

I decided to have a play around with it. My final goal was to get a car going which was followed by the camera, and I foolishly started doing that right away.
After a failed, I decided to take it one step at a time, building up to the final racer which was followed by the camera.

I got the car going, but realised that I wouldn't be able to tell if it was moving when I locked the camera onto it without a frame of reference, so I added tire tracks to trail behind the car.
Once I got that, I started with the car moving freely around, with the camera locked in place. After that, I locked the camera to the car, making sure to keep the tracks in the correct spot.
After that, I completely locked the camera to the back of the car, so you can se the tracks rotate around you.
The final step was adding some lag to the camera, which was an easy jump up.

You can see the progress through the different python files.
LockToPoint.py = The camera is stationary, and the car can move freely.
LockToCar.py = The camera follows the cars position, but not its rotation.
LockToBack.py = The camera follows behind the car exactly.
FollowCar.py = The camera follows behind the car, but there is a simulated delay so that multiple angles of the car can be viewed.

The amazing artwork I managed to find online, and is by Edu, who can be found here: https://edusilvart.itch.io/sprite-stack-cars
