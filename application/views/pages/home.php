<div class="container-fluid">
	<div class="row">
		<div class="col-md-12">
			<h3 class="text-center">
				Notes
			</h3>
			<?php foreach ($notes as $n){ ?>
			<a href="<?php echo base_url(); ?>View/show_note/<?php echo $n['note_id']; ?>"><button type="button" class="btn btn-lg btn-primary btn-block">
			<?php } ?>
              This Weeks Message
			</button></a><br />
			<a href="<?php echo base_url(); ?>View/show_previous"><button type="button" class="btn btn-lg btn-primary btn-block">
				Previous Messages
			</button></a>
		</div>
	</div>
</div>
