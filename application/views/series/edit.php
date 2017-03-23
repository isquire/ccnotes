<?php echo validation_errors(); ?>
<?php echo form_open('series/edit/'.$series['series_id'],array("class"=>"form-horizontal")); ?>

	<div class="form-group">
		<label for="series_title" class="col-md-4 control-label">Series Title</label>
		<div class="col-md-8">
			<input type="text" name="series_title" value="<?php echo ($this->input->post('series_title') ? $this->input->post('series_title') : $series['series_title']); ?>" class="form-control" id="series_title" />
		</div>
	</div>
	
	<div class="form-group">
		<div class="col-sm-offset-4 col-sm-8">
			<button type="submit" class="btn btn-success">Save</button>
        </div>
	</div>
	
<?php echo form_close(); ?>