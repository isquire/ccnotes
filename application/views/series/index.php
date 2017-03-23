<div class="pull-right">
	<a href="<?php echo site_url('series/add'); ?>" class="btn btn-success">Add</a> 
</div>

<table class="table table-striped table-bordered">
    <tr>
		<th>Series Id</th>
		<th>Series Title</th>
		<th>Actions</th>
    </tr>
	<?php foreach($series as $s){ ?>
    <tr>
		<td><?php echo $s['series_id']; ?></td>
		<td><?php echo $s['series_title']; ?></td>
		<td>
            <a href="<?php echo site_url('series/edit/'.$s['series_id']); ?>" class="btn btn-info">Edit</a> 
            <a href="<?php echo site_url('series/remove/'.$s['series_id']); ?>" class="btn btn-danger">Delete</a>
        </td>
    </tr>
	<?php } ?>
</table>