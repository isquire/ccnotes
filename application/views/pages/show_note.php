<div class="container-fluid">
	<div class="row">
		<div class="col-md-12">

			<h1>
				<?php echo $note['note_title'] ?>
			</h1>

				<?php
				foreach($all_series as $series)
				{
					$selected = ($series['series_id'] == $note['series_id']);

					echo $series['series_title'];
				}
				?>

			<p><?php echo $note['note_body'] ?></p>

		</div>
	</div>
	<div class="row">
		<div class="col-md-12">
			<a href="<?php echo base_url(); ?>">
				<button type="button" class="btn btn-lgs btn-primary">Back</button>
			</a>
		</div>
	</div>
</div>
