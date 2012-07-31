/*
* Video record with hdfvr and red5
* */

var userHasCamMic = function(cam_number,mic_number) {
    //alert("userHasCamMic("+cam_number+","+mic_number+")");
    //this function is called when HDFVR is initialized
};

var btRecordPressed = function() {
    //alert("btRecordPressed");
    //this function is called whenever the Record button is pressed to start a recording
};

var btStopRecordingPressed = function() {
    //alert("btStopRecordingPressed");
    //this function is called whenever a recording is stopped
};

var btPlayPressed = function() {
    //alert("btPlayPressed");
    //this function is called whenever the Play button is pressed to start/resume playback
};

var btPausePressed = function() {
    //alert("btPausePressed");
    //this function is called whenever the Pause button is pressed during playback
};

var onUploadDone = function(streamName,streamDuration,userId) {
    //alert("onUploadDone("+streamName+","+streamDuration+","+userId+")");

    //this function is called when the video/audio stream has been all sent to the video server and has been saved to the video server HHD,
    //on slow client->server connections, because the data can not reach the video server in real time, it is stored in the recorder's buffer until it is sent to the server, you can configure the buffer size in avc_settings.XXX

    //this function is called with 3 parameters:
    //streamName: a string representing the name of the stream recorded on the video server including the .flv extension
    //userId: the userId sent via flash vars or via the avc_settings.XXX file, the value in the avc_settings.XXX file takes precedence if its not empty
    //duration of the recorded video/audio file in seconds but acccurate to the millisecond (like this: 4.322)
};

var onSaveOk = function(streamName,streamDuration,userId,cameraName,micName) {
    //alert("onSaveOk("+streamName+","+streamDuration+","+userId+","+cameraName+","+micName+")");
    alert(auction_id);
    //the user pressed the [save] button inside the recorder and the save_video_to_db.XXX script returned save=ok
    $.post('/testimonials/video/send/', {'stream':streamName, auction:auction_id},function(data){

    });
};

var onSaveFailed = function(streamName,streamDuration,userId) {
    //alert("onSaveFailed("+streamName+","+streamDuration+","+userId+")");

    //the user pressed the [save] button inside the recorder but the save_video_to_db.XXX script returned save=fail
};

var onSaveJpgOk = function(streamName,userId) {
    //alert("onSaveJpgOk("+streamName+","+userId+")");

    //the user pressed the [save] button inside the recorder and the save_video_to_db.XXX script returned save=ok
};

var onSaveJpgFailed = function(streamName,userId) {
    //alert("onSaveJpgFailed("+streamName+","+userId+")");

    //the user pressed the [save] button inside the recorder but the save_video_to_db.XXX script returned save=fail
};

var onFlashReady = function () {
    //alert("onFlashReady()");
    //you can now comunicate with flash using the API
    //Example : document.VideoRecorder.record(); will make a call to flash in order to start recording
};


var onCamAccess = function(allowed) {

};

var VideoRecord2 = function(options) {
    var video_rec = {
        options: {
            id: undefined,
            volume_text: 'volume: ',
            container: undefined,
            video_class: 'video-rec',
            video_control_class: 'video-rec-control',
            quality: 'high',
            width: 320,
            height: 240,
            color: '#000000',
            swf_url: '',
            rtmp_server: 'rtmp://localhost/myapp/',
            publish: undefined,
            cam_size: '320x240'
            //cam_size: '640x480'
        },
        video: undefined,
        message_stop: undefined,
        has_record: false,
        message_block: function() {
            var self = this;
            $('#'+self.options.id+'-movie', self.video).css('visibility', 'hidden');
            self.video.block({ message: self.message_stop});
        },
        message_unblock: function(hidden) {
            var self = this;
            self.video.unblock();
            if (!hidden) {
                $('#'+self.options.id+'-movie', self.video).css('visibility', 'visible');
            }
        },
        __init__: function() {
            var self = this;
            var video = $("<div>");
            self.video = video;

            var src = 'VideoRecorder.swf?userId='+self.options.publish
                src += '&qualityurl=audio_video_quality_profiles/' +self.options.cam_size+'x30x90.xml'

            var flash_attrs = {
                id: self.options.id+'-movie',
                classid: "clsid:D27CDB6E-AE6D-11cf-96B8-444553540000",
                width: self.options.width,
                height: self.options.height,
                swf: self.options.swf_url+src,
                quality: self.options.quality,
                bgcolor: self.options.color,
                allowFullScreen: true,
                allowScriptAccess: 'always'
            };


            video.addClass(self.options.video_class);
            video.attr('id', self.options.id);
            video.css({width: self.options.width, display: 'block'});

            var container = $(self.options.container);
            container.append(video);
            video.flash(flash_attrs);

        }

    };
    video_rec.options = $.extend(video_rec.options, options);
    video_rec.__init__();
    return video_rec;
};