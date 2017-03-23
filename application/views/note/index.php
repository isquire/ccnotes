<div class="pull-right">
	<a href="<?php echo site_url('note/add'); ?>" class="btn btn-success"><span class="glyphicon glyphicon-plus" aria-hidden="true"></a> 
</div>

<table class="table table-striped table-bordered">
    <tr>
		<th>Note Id</th>
		<th>Note Title</th>
		<th>Note Body</th>
		<th>Note Date</th>
		<th>Series Id</th>
		<th>Speaker Id</th>
		<th>Actions</th>
    </tr>
	<?php foreach($notes as $n){ ?>
    <tr>
		<td><?php echo $n['note_id']; ?></td>
		<td><?php echo $n['note_title']; ?></td>
		<td><?php echo $n['note_body']; ?></td>
		<td><?php echo $n['note_date']; ?></td>
		<td><?php echo $n['series_id']; ?></td>
		<td><?php echo $n['speaker_id']; ?></td>
		<td>
            <a href="<?php echo site_url('note/edit/'.$n['note_id']); ?>" class="btn btn-info"><span class="glyphicon glyphicon-cog" aria-hidden="true"></span></a> 
            <a href="<?php echo site_url('note/remove/'.$n['note_id']); ?>" class="btn btn-danger"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></a>
        </td>
    </tr>
	<?php } ?>
</table>