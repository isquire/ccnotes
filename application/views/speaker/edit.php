<?php echo validation_errors(); ?>
<?php echo form_open('speaker/edit/'.$speaker['speaker_id'],array("class"=>"form-horizontal")); ?>
	<div class="form-group">
		<label for="speaker_name" class="col-md-4 control-label">Speaker Name</label>
		<div class="col-md-8">
			<input type="text" name="speaker_name" value="<?php echo ($this->input->post('speaker_name') ? $this->input->post('speaker_name') : $speaker['speaker_name']); ?>" class="form-control" class="form-control" id="speaker_name" />
		</div>
	</div>
	
	<div class="form-group">
		<div class="col-sm-offset-4 col-sm-8">
			<button type="submit" class="btn btn-success">Save</button>
        </div>
	</div>
	
<?php echo form_close(); ?>