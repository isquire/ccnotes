<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class View extends CI_Controller {

		function __construct()
		{
			parent::__construct();
			$this->load->model('Note_model');
		}


		public function index()
		{
			$data['notes'] = $this->Note_model->get_latest_note();

			$this->load->view('templates/header');
			$this->load->view('pages/home', $data);
			$this->load->view('templates/footer');
		}

		public function show_note($note_id)
		{
			$data['query'] = $this->Note_model->get_note($note_id);

			$this->load->view('templates/header');
			$this->load->view('pages/show_note' , $data);
			$this->load->view('templates/footer');
		}

  	public function show_previous()
    {
			$this->db->order_by('id', 'DESC');
			$data['query'] = $this->Note_model->get_all_notes();

     	$this->load->view('templates/header');
     	$this->load->view('pages/show_previous' , $data);
     	$this->load->view('templates/footer');
    }
}

?>
