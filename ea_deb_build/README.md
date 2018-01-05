Steps:

1. setup docker: https://developer.fedoraproject.org/tools/docker/docker-installation.html
2. docker build . -t eacirc_build_img
3. docker run --name=eacirc_build eacirc_build_img
   let the terminal run and from other, connect by:
4. docker exec -it eacirc_build bash
   do what you want in the image
        if you want to download files from image, use 
            docker cp eacirc_build:/home/eacuser/your/source_file ./host/copy_name

5. kill (ctrl+x) the docker run cmd and everything is done
