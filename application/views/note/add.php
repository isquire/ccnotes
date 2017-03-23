<?php echo validation_errors(); ?>
<?php echo form_open('note/add',array("class"=>"form-horizontal")); ?>

	<div class="form-group">
		<label for="note_title" class="col-md-4 control-label">Note Title</label>
		<div class="col-md-8">
			<input type="text" name="note_title" value="<?php echo $this->input->post('note_title'); ?>" class="form-control" id="note_title" />
		</div>
	</div>
	<div class="form-group">
		<label for="note_body" class="col-md-4 control-label">Note Body</label>
		<div class="col-md-8">
			<textarea name="note_body" class="form-control" id="note_body"><?php echo $this->input->post('note_body'); ?></textarea>
		</div>
	</div>
	<div class="form-group">
		<label for="note_date" class="col-md-4 control-label">Note Date</label>
		<div class="col-md-8">
			<input type="text" name="note_date" value="<?php echo $this->input->post('note_date'); ?>" class="form-control" id="note_date" placeholder="<?php echo date('Y-m-d'); ?>">
		</div>
	</div>
	<div class="form-group">
			<label for="series_id" class="col-md-4 control-label">Series Id</label>
			<div class="col-md-8">
				<select name="series_id" class="form-control">
					<option value="">select series</option>
					<?php 
					foreach($all_series as $series)
					{
						$selected = ($series['series_id'] == $this->input->post('series_id')) ? ' selected="selected"' : "";

						echo '<option value="'.$series['series_id'].'" '.$selected.'>'.$series['series_title'].'</option>';
					} 
					?>
				</select>
			</div>
		</div>
	<div class="form-group">
			<label for="speaker_id" class="col-md-4 control-label">Speaker Id</label>
			<div class="col-md-8">
				<select name="speaker_id" class="form-control">
					<option value="">select speaker</option>
					<?php 
					foreach($all_speaker as $speaker)
					{
						$selected = ($speaker['speaker_id'] == $this->input->post('speaker_id')) ? ' selected="selected"' : "";

						echo '<option value="'.$speaker['speaker_id'].'" '.$selected.'>'.$speaker['speaker_name'].'</option>';
					} 
					?>
				</select>
			</div>
		</div>
	
	<div class="form-group">
		<div class="col-sm-offset-4 col-sm-8">
			<button type="submit" class="btn btn-success">Save</button>
        </div>
	</div>

<?php echo form_close(); ?>