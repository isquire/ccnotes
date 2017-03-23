<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>CCNotes</title>

	<script src="//cloud.tinymce.com/stable/tinymce.min.js?apiKEY=4vpt1vqiz3nzcny7m429fr34ia3oingfdjambnms8c912jaz"></script>
	<script>
	tinymce.init({
  selector: 'textarea',
  height: 500,
  menubar: true,
  plugins: [
    'advlist autolink lists link image charmap print preview anchor',
    'searchreplace visualblocks code fullscreen',
    'insertdatetime media table contextmenu paste code'
  ],
  toolbar: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
  content_css: '//www.tinymce.com/css/codepen.min.css'
});
	</script>

    <!-- Bootstrap
    <link href="<?php echo base_url(); ?>resource/bootstrap/css/bootstrap.min.css" rel="stylesheet">-->
    <link href="http://bootswatch.com/flatly/bootstrap.min.css" rel="stylesheet">




    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>

  <div class="container-fluid">
  	<div class="row">
  		<div class="col-md-12">

  		<ul class="nav nav-pills">
          <li>
            <a href="<?php echo base_url(); ?>View">Home</a>
          </li>
  				<li>
  					<a href="<?php echo base_url(); ?>Note">Notes</a>
  				</li>
  				<li>
  					<a href="<?php echo base_url(); ?>Series">Series</a>
  				</li>
  				<li>
  					<a href="<?php echo base_url(); ?>Speaker">Speakers</a>
  				</li>
  				<li>
  					<a target="_blank" href="<?php echo base_url(); ?>user_guide">User Guide</a>
  				</li>
			</ul>
