<div class="container-fluid">
	<div class="row">
		<div class="col-md-12">

			<h1><?php echo $query['note_title'] ?> <small><?php echo $query['note_date'] ?></small></h1>
			<p><?php echo $query['note_body'] ?></p>

		<a href="<?php echo base_url(); ?>">
			<button type="button" class="btn btn-lgs btn-primary">Back</button>
		</a>

		</div>
	</div>
</div>
