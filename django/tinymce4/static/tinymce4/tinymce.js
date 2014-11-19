/*
TODO: Split in generic config and local config
      tinymce.init is mostly local config

console.log (django.jQuery);
// These does the same
console.log (tinymce);
console.log (tinyMCE);
*/

//    var csrf = $cookie ('csrftoken');

function $get (id) {
    return document.getElementById (id);
}


document.addEventListener ("DOMContentLoaded", function (event)
{
    event.target.body.innerHTML +=
        '<form id="tinymce-upload-form" action="/tinymce/upload/" method="post" enctype="multipart/form-data" style="display:none">' +
        '  <input type="file" id="tinymce-file-input" name="must-have-a-name" />' +
        '</form>';
});



function ajax_upload (form, on_load, on_error)
{
    var xhr = new XMLHttpRequest();
    if (on_load)
	xhr.onload = on_load;
    if (on_error)
	xhr.onerror = on_error;
    else
	xhr.onerror = function (ev) { error('ajax_upload', arguments, ev); }

    xhr.open ('POST', form.getAttribute('action'));
    xhr.setRequestHeader ('X-REQUESTED-WITH', 'XMLHttpRequest');
    xhr.send (new FormData(form));
}


function tinymce_upload (form, output)
{
    ajax_upload (form, function (ev) {
	var response = ev.target.responseText;
	var A = response.split (' ', 2);
	console.assert (A[0]=='OK', 'upload error:', response.substring(0,4096));
	output.value = A[1];
    });
}


/** TinyMCE4 config. */
tinymce.init ({
    selector: 'textarea.tinymce',

    width: 800,
    height: 450,
    resize: 'both',

    entity_encoding : "raw",
    custom_undo_redo_levels: 8,

    menubar: 'edit insert format table',
    // Default is: 'tools table format view insert edit'

    toolbar: 'undo redo | styleselect | bold italic forecolor | alignleft aligncenter alignright | bullist numlist outdent indent blockquote | link image | code',
    // Default is: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image'

    plugins: ['image', 'link', 'paste', 'anchor', 'code', 'table', 'textcolor'],

    /* Note: will override defaults
    // Defaults: http://www.tinymce.com/wiki.php/Configuration:style_formats
    style_formats: [
	{title: 'Ingress', block: 'div', classes: 'ingress'},
	{title: 'Tittel', block: 'h1', styles: {color: 'green'}},
	{title: 'Row border', selector: 'tr', classes: 'foobar'},
	// @note selector can be complex css selector. e.g., odd rows in
	// a table.
    ],
    */

    /** Plugin config */

    // Link
    link_list: [
	{title: 'Blogg',	value: 'http://blogg.normal.no'},
	{title: 'Facebook',	value: 'https://www.facebook.com/NormalNorway'},
	{title: 'Youtube',	value: 'http://www.youtube.com/user/normalnorway'},
	{title: 'Nyhetsbrev',	value: 'http://eepurl.com/S3rFH'},
	{title: 'Donér',	value: 'alert("todo")'},
    ],

    // Image
    image_list: [
	{title: 'Logo',         value: '/static/images/logo.png'},
	{title: 'Logo (liten)', value: '/static/images/logo-300.png'},
    ],
    image_advtab: true,

    file_browser_callback: function (field_name, url, type, win)
    {
	if (type != 'image') return;
	var el = $get ('tinymce-file-input');
	el.onchange = function (ev) {
	    //file = ev.target.files[0];
	    tinymce_upload (ev.target.form, $get (field_name));
	};
	el.click();
    }
});