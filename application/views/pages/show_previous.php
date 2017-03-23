<div class="container-fluid">
	<div class="row">
		<div class="col-md-12">

      <br />

      <div class="list-group">
        <?php foreach ($query as $item):?>
          <a href="<?php echo base_url(); ?>Notes/show_note/<?php echo $item->id; ?>" class="list-group-item">
            <h4 class="list-group-item-heading"><?php echo $item->title; ?></h4>
            <p class="list-group-item-text"><?php echo $item->create_date; ?></p>
          </a>
        <?php endforeach;?>
      </div>

      <a href="<?php echo base_url(); ?>">
        <button type="button" class="btn btn-lgs btn-primary">Back</button>
      </a>

    </div>
  </div>
</div>
