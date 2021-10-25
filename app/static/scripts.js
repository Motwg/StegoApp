
let openModal = img => {
  let modal = document.getElementById("modal-div");
  let modalImg = document.getElementById("modal-img");
  modal.style.display = "block";
  modalImg.src = img.src;
}

let openProgressModal = () => {
  let modal = document.getElementById("modal-bar");
  modal.style.display = "block";
}

let closeModal = mod_id => {
  let modal = document.getElementById(mod_id);
  modal.style.display = "none";
}

let slideDelta = (sl, id) => {
  document.getElementById(id).innerHTML = "Current value: " + sl.value;
}


$(document).ready(() => {
    var percentage = 0; // loading bar percentage
    const socket = io("/events");

    socket.on('progress', progress => {
        percentage = progress;
    });

    let startProgressBar = () => {
        openProgressModal()
        let processProgressBar = (timer) => {
            $(".progress-bar").css("width", percentage + "%");
        }

        let timer = setInterval(() => {
            socket.emit('check_progress_bar');
            processProgressBar(timer);
        }, 250);

        return timer // timer needs to be stopped by stopProgressBar function
    }

    let stopProgressBar = timer => {
        clearInterval(timer);
        socket.emit('reset_progress_bar');
        closeModal("modal-bar");
        $('.progress-bar').css('width', '0%');
    }

    let scheme = {
        'lsb': ['channel'],
        'none': [],
        'qim': ['channel', 'delta'],
        'dc_qim': ['channel', 'delta', 'alpha']
    };

    // auto hiding/showing options
    $("form#embedding :input[name='algorithm']").each(function() {
        let alg = $(this);
        alg.change(() => {
            $("form#embedding :input[name!='algorithm'][name]").map(function() {
                let input = $(this);
                if(scheme[alg.val()] && scheme[alg.val()].includes(input.attr('name'))) {
                    input.parent().show();
                }
                else {
                    input.parent().hide();
                };
            });
        });
    });

    $("form#extract :input[name='algorithm']").each(function() {
        let alg = $(this);
        alg.change(() => {
            $("form#extract :input[name!='algorithm'][name]").map(function() {
                let input = $(this);
                if(scheme[alg.val()] && scheme[alg.val()].includes(input.attr('name'))) {
                    input.parent().show();
                }
                else {
                    input.parent().hide();
                };
            });
        });
    });


    $("#upload-image").change(e => {
        let file_data = $("#upload-image").prop("files")[0];
        let form_data = new FormData();
        form_data.append("upload-image", file_data);
        e.preventDefault();
        let timer = startProgressBar();
        $.ajax({
            type:'POST',
            url:'/demo/uploader/image',
            data: form_data,
            processData: false,
            contentType: false,
            success: response => {
                // refresh standard img
                $("#upImg").attr("src", response.img);
            },
            error: err => {
                console.log(err.responseJSON);
                alert(err.responseJSON.msg);
            },
            complete: () => {
                stopProgressBar(timer);
            }
        });
    });


    $("#upload-mod").change(e => {
        let file_data = $("#upload-mod").prop("files")[0];
        let form_data = new FormData();
        form_data.append("upload-mod", file_data);
        e.preventDefault();
        let timer = startProgressBar();
        $.ajax({
            type:'POST',
            url:'/demo/uploader/mod',
            data: form_data,
            processData: false,
            contentType: false,
            success: response => {
                // refresh modified img
                $("#modImg").attr("src", response.img);
            },
            error: err => {
                console.log(err.responseJSON);
                alert(err.responseJSON.msg);
            },
            complete: () => {
                stopProgressBar(timer);
            }
        });
    });


    $("#btn-embed").click(e => {
        // auto fill extraction options
        $("form#embedding :input").each(function() {
             let input = $(this);
             if (input.attr('name')) {
                $("form#extract :input[name=" + input.attr('name') + "]").val(input.val())
             }
        });
        $("form#extract :input[name='algorithm']").trigger("change")
        $("form#extract :input[name='delta']").trigger("change")
        $("form#extract :input[name='alpha']").trigger("change")

        let form_data = new FormData($('#embedding')[0]);
        // add image as b64 to form
        let file_data = $("#upImg").attr('src');
        form_data.append("up_img", file_data);

        e.preventDefault();
        let timer = startProgressBar();
        $.ajax({
            type:'POST',
            url:'/demo/embedding',
            processData: false,
            contentType: false,
            data: form_data,
            success: response => {
                // refresh embedded img
                $("#embImg").attr("src", response.img);
                $("#download-file").attr("href", response.img);
            },
            error: err => {
                console.log(err.responseJSON);
                alert(err.responseJSON.msg);
            },
            complete: () => {
                stopProgressBar(timer);
            }
        });
    });


    $("#btn-mod").click(e => {
        let form_data = new FormData($('#modification')[0]);
        // add image as b64 to form
        let file_data = $("#embImg").attr('src');
        form_data.append("emb_img", file_data);

        e.preventDefault();
        let timer = startProgressBar();
        $.ajax({
            type:'POST',
            url:'/demo/modify',
            processData: false,
            contentType: false,
            data: form_data,
            success: response => {
                // refresh modified img
                $("#modImg").attr("src", response.img);
            },
            error: err => {
                console.log(err.responseJSON);
                alert(err.responseJSON.msg);
            },
            complete: () => {
                stopProgressBar(timer);
            }
        });
    });


    $("#btn-extract").click(e => {
        let form_data = new FormData($('#extract')[0]);
        // add image as b64 to form
        let file_data = $("#modImg").attr('src');
        form_data.append("mod_img", file_data);

        e.preventDefault();
        let timer = startProgressBar();
        $.ajax({
            type:'POST',
            url:'/demo/extract',
            processData: false,
            contentType: false,
            data: form_data,
            success: response => {
                $("#ext-watermark").val(response.watermark);
            },
            error: err => {
                console.log(err.responseJSON);
                alert(err.responseJSON.msg);
            },
            complete: () => {
                stopProgressBar(timer);
            }
        });
    });

    let detectWatermark = (det, prob) => {
        let text = "";
        if(det === "0") {
            text = "Watermark not detected ";
        }
        else {
            text = "Watermark detected ";
        }
        return text + "(" + prob + "%)";
    };

    $("#btn-steganalysis").click(e => {
        let form_data = new FormData($("#steganalysis")[0]);
        // add image as b64 to form
        let file_data = $("#embImg").attr('src');
        form_data.append("emb_img", file_data);

        e.preventDefault();
        let timer = startProgressBar();
        $.ajax({
            type:'POST',
            url:'/demo/steganalysis',
            processData: false,
            contentType: false,
            data: form_data,
            success: response => {
                $('#red').html(detectWatermark(response.r, response.r_p));
                $('#green').html(detectWatermark(response.g, response.g_p));
                $('#blue').html(detectWatermark(response.b, response.b_p));
                $('#steganalysisModal').modal();
            },
            error: err => {
                console.log(err.responseJSON);
                alert(err.responseJSON.msg);
            },
            complete: () => {
                stopProgressBar(timer);
            }
        });
    });
});
