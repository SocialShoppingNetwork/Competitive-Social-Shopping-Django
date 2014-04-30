<?php
//this file is called by the videorecorder.swf file when the [SAVE] button is pressed
//3 variables are passed to this file via GET:
//the streamName var  contains the name of the .flv file as it is on the REd5/FMS server on which it was saved
//the streamDuration var  contains the duration of the video stream in seconds but it is accurate to the millisecond  like this: 4.231
//the userId GET var contains the value of the userId GET var sent from avc_settings.php or via flash vars, if userId si found in both places the one in avc_settings.php is used
//you can do whatever you want in here with the variables like insert them in a db etc..


$streamName=$_GET["streamName"];
$streamDuration=$_GET["streamDuration"];
$userId= $_GET["userId"];

echo "save=ok";
//echo "save=failed" to tell the recorder the save has failed and display the save button again
?>