<div class="pull-right">
	<a href="<?php echo site_url('series/add'); ?>" class="btn btn-success"><span class="glyphicon glyphicon-plus" aria-hidden="true"></a>
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
            <a href="<?php echo site_url('series/edit/'.$s['series_id']); ?>" class="btn btn-info"><span class="glyphicon glyphicon-cog" aria-hidden="true"></a>
            <a href="<?php echo site_url('series/remove/'.$s['series_id']); ?>" class="btn btn-danger"><span class="glyphicon glyphicon-remove" aria-hidden="true"></a>
        </td>
    </tr>
	<?php } ?>
</table>
