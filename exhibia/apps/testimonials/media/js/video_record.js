var recordStarted = function() {
    alert("record started");
};

var recordStopped = function() {
    alert("record has stopped");
    // is called when recording is stopped
};

var VideoRecord = function(options) {
    var hasVersion10 = DetectFlashVer(10, 0, 0);
    var hasVersion10_3 = DetectFlashVer(10, 3, 0);
    var VideoIO = (hasVersion10_3 ? "VideoIO45.swf" : (hasVersion10 ? "VideoIO.swf" : null));
    var video_rec = {
        options: {
            id: undefined,
            volume_text: 'volume: ',
            container: undefined,
            video_class: 'video-rec',
            video_control_class: 'video-rec-control',
            quality: 'high',
            flashVars: '',
            width: 320,
            height: 240,
            color: '#000000',
            swf_url: '',
            rtmp_server: 'rtmp://localhost/myapp/',
            publish: undefined,
            publish_fn: undefined,
            microRate: undefined,
            fps: undefined,
            noVideo: 'false'
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
            var video = $("<div>"),
                video_obj = $("<div>"),
                video_control = $("<div>");
            self.video = video;

            var attrs = {
                id: self.options.id+'-movie',
                width: self.options.width,
                height: self.options.height
            };

            video_obj.attr(attrs);

            var flashVars = 'noVideo=' + self.options.noVideo +
                        '&showBar=false&backToRecorder=false&server='+ self.options.rtmp_server +
                        '&fileName='+ self.options.publish
            if (self.options.microRate)
                flashVars += '&microRate='+ self.options.microRate;
            if (self.options.fps)
                flashVars += '&fps='+ self.options.fps;

            var params = {
                movie: self.options.swf_url+'red5recorder.swf',
                quality: self.options.quality,
                bgcolor: self.options.color,
                flashVars: self.options.flashVars,
                allowFullScreen: true,
                allowScriptAccess: 'always',
                FlashVars: flashVars
            };

            /*buttons*/
            var record_btn = $('<span>');
            record_btn.append($('<span>').addClass('icon'));
            record_btn.addClass('video-rec-button').addClass('record').addClass('record-start');
            record_btn.appendTo(video_control);
            var play_btn = $('<span>');
            play_btn.append($('<span>').addClass('icon'));
            play_btn.addClass('video-rec-button').addClass('play_video').addClass('play_video-on');
            play_btn.appendTo(video_control);

            var play_pause_btn = $('<span>');
            play_pause_btn.append($('<span>').addClass('icon'));
            play_pause_btn.addClass('video-rec-button').addClass('play_pause').addClass('play_pause-pause');
            play_pause_btn.appendTo(video_control);

            var stop_btn = $('<span>');
            stop_btn.append($('<span>').addClass('icon'));
            stop_btn.addClass('video-rec-button').addClass('stop');
            stop_btn.appendTo(video_control);

            var volume_control = $('<span>');
            volume_control.addClass('video-rec-button').addClass('volume');
            var volumen_slider = $('<div>').addClass('volume-slider');
            volumen_slider.appendTo(volume_control);
            var volumen_amount_title = $('<span>').addClass('volume-amount-title').text(self.options.volume_text);
            var volumen_amount_value = $('<span>').addClass('volume-amount-value').text('60');
            var volumen_amount = $('<div>').addClass('volume-amount').append(volumen_amount_title).append(volumen_amount_value);
            volumen_amount.appendTo(volume_control);
            volume_control.append($('<div>').css({clear: 'both', width:0, height: 0}));
            volume_control.appendTo(video_control);


            video_control.addClass(self.options.video_control_class);

            video.addClass(self.options.video_class);
            video.attr('id', self.options.id);
            //video.css('background-color', self.options.color);
            video.css({width: self.options.width, display: 'block'});

            var container = $(self.options.container);
            container.append(video);
            video.append(video_obj);
            swfobject.embedSWF(self.options.swf_url+'red5recorder.swf', self.options.id+'-movie',
                        self.options.width, self.options.height, '10.0.0',
                        self.options.swf_url+'playerProductInstall.swf', '', params, attrs);
            video_control.appendTo(video);

            var preview_video = function () {
                self.message_unblock();
                var obj = self.get_flash_movie();
                obj.stopRecording();
                obj.playRecording();
                obj.setVolume(volumen_amount_value.text());
                play_btn.addClass('play_video-off').removeClass('play_video-on');
                stop_btn.show();
                volume_control.show();
                play_pause_btn.show();
            };

            var publish_video = function () {
                if(self.options.publish_fn) {
                    self.options.publish_fn(self, init_video);
                }else {
                    init_video();
                }
            };

            var init_video = function() {
                self.has_record = false;
                play_btn.addClass('play_video-on').removeClass('play_video-off');
                record_btn.addClass('record-start').removeClass('record-stop');
                record_btn.show();
                play_btn.hide();
                stop_btn.hide();
                volume_control.hide();
                play_pause_btn.hide();
                self.message_unblock();
            };

            var record_start = function() {
                var obj = self.get_flash_movie();
                obj.startRecording();
                play_btn.addClass('play_video-on').removeClass('play_video-off');
                stop_btn.hide();
                volume_control.hide();
                play_pause_btn.hide();
            }

            var re_recorded_video = function () {
                if(confirm('Override last capture?')) {
                    record_start();
                    play_btn.hide();
                }
                self.message_unblock();
            };


            var message_stop = $('<div>').hide();
            var preview_btn = $('<input>').attr({type: 'button', value: 'preview'}).click(function() {
                preview_video();
            });
            var publish_btn = $('<input>').attr({type: 'button', value: 'publish'}).click(function() {
                publish_video();
            });
            var re_recorded_btn = $('<input>').attr({type: 'button', value: 're-recorded'}).click(function() {
                re_recorded_video();
            });
            message_stop.append(preview_btn);
            message_stop.append(publish_btn);
            message_stop.append(re_recorded_btn);
            message_stop.appendTo(video);
            self.message_stop = message_stop;

            /*events*/
            init_video();

            recordStarted = function() {
                self.has_record = true;
                record_btn.addClass('record-stop').removeClass('record-start');
            };

            recordStopped = function() {
                play_btn.show();
                record_btn.addClass('record-start').removeClass('record-stop');
            };

            $('.record-start', $('#'+self.options.id)).live('click', function() {
                if(self.has_record) {
                    re_recorded_video();
                } else {
                    record_start();
                }
            });

            $('.record-stop', $('#'+self.options.id)).live('click', function() {
                var obj = self.get_flash_movie();
                obj.stopRecording();
                if(self.has_record) {
                    self.message_block();
                }
            });

            $('.play_video-on', $('#'+self.options.id)).live('click', function() {
                preview_video();
            });

            $('.play_video-off', $('#'+self.options.id)).live('click', function() {
                var obj = self.get_flash_movie();
                obj.stopRecording();
                stop_btn.hide();
                volume_control.hide();
                play_pause_btn.hide();
                $(this).addClass('play_video-on').removeClass('play_video-off');
                if(self.has_record) {
                    self.message_block();
                }
            });

            $('.play_pause', $('#'+self.options.id)).live('click', function() {
                var obj = self.get_flash_movie();
                obj.playPause();
                if($(this).hasClass('play_pause-pause'))
                    $(this).addClass('play_pause-play').removeClass('play_pause-pause');
                else
                    $(this).addClass('play_pause-pause').removeClass('play_pause-play');
            });

            $('.stop', $('#'+self.options.id)).live('click', function() {
                var obj = self.get_flash_movie();
                obj.stopVideo();
                play_pause_btn.addClass('play_pause-pause').removeClass('play_pause-play');
            });

            volumen_slider.slider({
                orientation: "horizontal",
                range: "min",
                min: 0,
                max: 100,
                value: 60,
                slide: function( event, ui ) {
                    volumen_amount_value.text( ui.value );
                    var obj = self.get_flash_movie();
                    obj.setVolume(ui.value);
                }
            });

        },
        get_flash_movie: function(){
            var self = this;
            var movieName = self.options.id+'-movie';
            var isIE = navigator.appName.indexOf("Microsoft") != -1;
            return (isIE) ? window[movieName] : document[movieName];
        }

    };
    video_rec.options = $.extend(video_rec.options, options);
    video_rec.__init__();
    return video_rec;
};