class pip_install (
  $path_requirements_file,
) {

  exec { "pip_requirements_install": command => "pip install -r ${path_requirements_file}", refreshonly => true, }

}