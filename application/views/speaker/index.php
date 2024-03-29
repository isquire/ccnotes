<div class="pull-right">
	<a href="<?php echo site_url('speaker/add'); ?>" class="btn btn-success"><span class="glyphicon glyphicon-plus" aria-hidden="true"></a>
</div>

<table class="table table-striped table-bordered">
    <tr>
		<th>Speaker Id</th>
		<th>Speaker Name</th>
		<th>Actions</th>
    </tr>
	<?php foreach($speaker as $s){ ?>
    <tr>
		<td><?php echo $s['speaker_id']; ?></td>
		<td><?php echo $s['speaker_name']; ?></td>
		<td>
            <a href="<?php echo site_url('speaker/edit/'.$s['speaker_id']); ?>" class="btn btn-info"><span class="glyphicon glyphicon-cog" aria-hidden="true"></a>
            <a href="<?php echo site_url('speaker/remove/'.$s['speaker_id']); ?>" class="btn btn-danger"><span class="glyphicon glyphicon-remove" aria-hidden="true"></a>
        </td>
    </tr>
	<?php } ?>
</table>
