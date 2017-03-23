<div class="container-fluid">
	<div class="row">
		<div class="col-md-12">

		<?php foreach ($query as $n): ?>
			<h1><?php echo $n->note_title; ?> <small><?php echo $n->note_date; ?></small></h1>
			<p><?php echo $n->note_body; ?></p>
		<?php endforeach; ?>

		<a href="<?php echo base_url(); ?>">
			<button type="button" class="btn btn-lgs btn-primary">Back</button>
		</a>

		</div>
	</div>
</div>
