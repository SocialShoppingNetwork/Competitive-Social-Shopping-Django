<%
''###################### HDFVR Configuration File #####################

''connectionstring:String
''desc: the rtmp connection string to the hdfvr application on your media server
''values: 'rtmp:''localhost/hdfvr/_definst_', 'rtmp:''myfmsserver.com/hdfvr/_definst_', etc...
Dim connectionstring
connectionstring=""

''languagefile:String
''description: path to the XML file containing words and phrases to be used in the video recorder interface, use this setting to switch between languages while maintaining several language files
''default: "translations/en.xml"
Dim languagefile
languagefile="translations/en.xml"

''qualityurl: String
''desc: path to the .xml file describing video and audio quality to use for recording, this variable has higher priority than the qualityurl from flash vars
''values: URL paths to the audio/video quality profile files
Dim qualityurl
qualityurl=""

''maxRecordingTime: Number
''desc: the maximum recording time in seconds
''values: any number greater than 0
Dim maxRecordingTime
maxRecordingTime=120

''userId: String
''desc: the id of the user logged into the website, not mandatory, this var is passed back to the save_video_to_db.php file via GET when the [SAVE] button in the recorder is pressed. This variable can also be passed via flash vars like this: videorecorder.swf?userId=XXX, but the value in this file, if not empty, takes precedence.
''values: strings or numbers will do
''default: ""
Dim userId
userId = ""

''outgoingBuffer: Number
''desc: Specifies how long the buffer for the outgoing data can grow before Flash Player starts dropping frames. On a high-speed connection, buffer time shouldn't be a concern data is sent almost as quickly as Flash Player can buffer it. On a slow connection, however, there might be a significant difference between how fast Flash Player buffers the data and how fast it can be sent to the client. Only affects the recording process of the recorder!
''values: 30,60,etc...
''default:60
Dim outgoingBuffer
outgoingBuffer=60

''playbackBuffer: Number
''desc: Specifies how much video time to buffer when (after recording a movie) you play it back
''values: 1, 10,20,30,60,etc...
''default:1
Dim playbackBuffer
playbackBuffer=1

''autoPlay: String
''desc: weather the recorded video should play automatically after recording it or we should  wait for the user to press the PLAY button
''values: false, true
''default: false
Dim autoPlay
autoPlay="false"

''deleteUnsavedFlv: String
''desc: weather the recorded video should be deleted  from the server if the client does not press save
''values: false, true
''default: false
Dim deleteUnsavedFlv
deleteUnsavedFlv = "false"

''hideSaveButton:Number
''desc: makes the [SAVE] button invisible. When the [SAVE] button is pressed the save_video_to_db.xxx script is called and the corresponding JS functions. The creation/existence of the new video file and corresponding snapshot do not depend on pressing this button.
''An invisible SAVE button can be used to move the SAVE action to the HTML page where there can be other form fileds that can be submitted together with the info about the vid.
''When the SAVE button is hidden you can use the onUploadDone java script hook to get some info about the newly recorded flv file and redirect the user/enable a button on the HTML page/populate some hidden FORM vars/etc... .
''NOTE: when hiding this button some functions/calls will never be performed: save_video_to_db.php will never be called, onSaveOk and onSaveFailed JS functions will not be called, onSaveJpgFailed and onSaveJpgOk will not be called
''values: 1 for hidden, 0 for visible
''deault: 0
Dim hideSaveButton
hideSaveButton=0

''onSaveSuccessURL:String
''desc: when the [SAVE] button is pressed (if its enabled) save_video_to_db.php is called. If the save operation succeeds AND if this variable is NOT EMPTY, the user will be taken to the URL described in this URL
''values: 
''deault:""
Dim onSaveSuccessURL
onSaveSuccessURL=""

''snapshotSec:Number
''desc: the snapshot is taken when the recording reaches this length/time
''NOTE: THE SNAPSHOT IS SAVED TO THE WEB SERVER AS A JPG WHEN THE USER PRESSES THE SAVE BUTTON. If Save is not pressed the snapshot is not saved.
''values: any number  greater or equal to 0,  if 0 then the snap shot is taken when the [REC] button is pressed
Dim snapshotSec
snapshotSec = 5

''snapshotEnable:Number
''desc: if set to true the recorder will take a snapshot 
''values: true or false
Dim snapshotEnable
snapshotEnable = "true"

''minRecordTime:Number
''desc: the minimum number of seconds a recording must be in length. The STOP button will be disabled until the recording reaches this length!
''values: any number lower them maxRecordingTime
''default:5
Dim minRecordTime
minRecordTime = 5

''backgroundColor:Hex number
''desc: color of background area inside the video recorder around the video area
''values: any color in hex format
''default:0x990000 (dark red)
Dim backgroundColor
backgroundColor = "0x990000"

''menuColor:Hex number
''desc: the color of the lower area of the recorder containing the buttons and the scrub bar
''values: any color in hex format
''default:default:0x333333 (dark grey)
Dim menuColor
menuColor = "0x333333"

''radiusCorner:Number
''Desc: the radius of the 4 corners of the video recorder
''values: 0 for no rounded corners, 4,8,16,etc...
''default: 4
Dim radiusCorner
radiusCorner = 4

''showFps:String
''desc: "false" to hide it "true" to show it
''values: true or false
''default: true
Dim showFps
showFps = "true"

''recordAgain:String
''desc:if set to true the user will be able to record again and again until he is happy with the result. If set to false he only has 1 shot!
''values:"false" for one recording, "true" for multiple recordings
''default: "true"
Dim recordAgain
recordAgain =  "true"

''useUserId:String
''desc:if set to "true" the stream name will be {userId}_{timestamp_random}
''values:"false" for not using the userId in the file name, "true" for using it
''default: "false"
Dim useUserId
useUserId =  "false"

''streamPrefix:String
''desc: adds a prefix to the .flv (recording) file name on the media server like this: {prefix}_{userId}_{timestamp_random} or {prefix}_{timestamp_random} if the useUserId option is set to false
''values: a string
''default: ""
Dim streamPrefix
streamPrefix = ""

''streamName:String
''desc: By default the application generates a random name ({prefix}_{userId}_{timestamp_random}) for the .flv file (recording). If you want to use a certain name set this variable and it will overwrite the pattern {prefix}_{userId}_{timestamp_random} 
''values: a string
''default: ""
Dim streamName
streamName = ""

''disableAudio:String
''desc: By default the application records audio and video. If you want to disable audio recording set this var to "true".
''values: "false" to include audio in the recording, "true" to record without audio
''default: "false"
Dim disableAudio
disableAudio = "false"

''chmodStreams:String
''desc: If you want to change the permissions on the newly recorded .flv file after it is saved to the disk on the media server you can use this variable. This works only on Red5 and Wowza.
''values: "0666","0777", etc.
''default: ""
Dim chmodStreams
chmodStreams = ""

''padding:Number
''desc: the padding between elements in the recorder in pixels
''values: any number
''default:2
Dim padding
padding = 2

''countdownTimer
''desc: set to true if you want the timer to decrease from the upper limit (maxRecordingTime) down to 0
''values: "true", "false"
''default: "false"
Dim countdownTimer
countdownTimer = "false"

''overlayPath:String
''desc: realtive URL path to the image to be shown as overlay
''values: any realtive path
''defaut: "" no overlay
Dim overlayPath
overlayPath = ""

''overlayPosition:String
''desc: position of the overlay image mentioned above
''values: "tr" for top right
''defaut: "tr"
Dim overlayPosition
overlayPosition="tr"

''loopbackMic:String
''desc: weather or not the sound should be also played back in the speakers/heaphones during recording
''values: "true" for ye, "false" for no
''defaut: "false"
Dim loopbackMic
loopbackMic="false"

''showMenu:String
''desc: weather or not the bottom menu in the HDFVR shoud show, some people choose to control the HDFVR via JS and they do ot need the menu, when not using the menu you can decrease the height of HDFVR by 32 (3o is the height of the button 2 is the default padding value in this config file)
''values: "true" to show, "false" to hide
''default: "true"
Dim showMenu
showMenu="true"


''##################### DO NOT EDIT BELOW ############################
Response.write("connectionstring=")
Response.write(connectionstring)
Response.write("&languagefile=")
Response.write(languagefile)
Response.write("&qualityurl=")
Response.write(qualityurl)
Response.write("&maxRecordingTime=")
Response.write(maxRecordingTime)
Response.write("&userId=")
Response.write(userId)
Response.write("&outgoingBuffer=") 
Response.write(outgoingBuffer)
Response.write("&playbackBuffer=") 
Response.write(playbackBuffer)
Response.write("&autoPlay=")
Response.write(autoPlay)
Response.write("&deleteUnsavedFlv=")
Response.write(deleteUnsavedFlv)
Response.write("&hideSaveButton=")
Response.write(hideSaveButton)
Response.write("&onSaveSuccessURL=")
Response.write(onSaveSuccessURL)
Response.write("&snapshotSec=")
Response.write(snapshotSec)
Response.write("&snapshotEnable=")
Response.write(snapshotEnable)
Response.write("&minRecordTime=")
Response.write(minRecordTime)
Response.write("&backgroundColor=")
Response.write(backgroundColor)
Response.write("&menuColor=")
Response.write(menuColor)
Response.write("&radiusCorner=")
Response.write(radiusCorner)
Response.write("&showFps=")
Response.write(showFps)
Response.write("&recordAgain=")
Response.write(recordAgain)
Response.write("&useUserId=")
Response.write(useUserId)
Response.write("&streamPrefix=")
Response.write(streamPrefix)
Response.write("&streamName=")
Response.write(streamName)
Response.write("&disableAudio=")
Response.write(disableAudio)
Response.write("&chmodStreams=")
Response.write(chmodStreams)
Response.write("&padding=")
Response.write(padding)
Response.write("&overlayPath=")
Response.write(overlayPath)
Response.write("&overlayPosition=")
Response.write(overlayPosition)
Response.wrote("&loopbackMic=")
Response.write(loopbackMic)
Response.write("&showMenu=")
Response.write(showMenu)

%>