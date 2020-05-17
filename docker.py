

def write_docker_file(docker, ip, date_string):
    dockerfile = "reports/" + date_string + "/docker.txt"

    with open(dockerfile, "a+") as docker_file:
        docker_file.write(ip + "\n")

        if docker['Containers']:
            for container in docker['Containers']:
                docker_file.write("\tImage: {}\n".format(container['Image']))
                docker_file.write("\tID: {}\n".format(container['Id']))
                docker_file.write("\tCommand: {}".format(container['Command']))
                docker_file.write("\tCreated:{}\n".format(container['Created']))
                docker_file.write("Names: \n")

                for name in container['Names']:
                    docker_file.write("\t{}\n".format(name))

                docker_file.write("\tStatus: {}\n".format(container['Status']))
                docker_file.write("Ports:\n")

                for port in container['Ports']:
                    docker_file.write("\t{}\n".format(port))
        elif docker['Containers'] == "":
            pass
        else:
            pass

        # docker_file.write("COMPONENTS: \n")
        # for components in docker['Components']:
        #     docker_file.write("{}\n".format(components['Name']))
        #     docker_file.write('\tDetails:\n')
        #     # docker_file.write("\t\tExperimental: {}\n".format(components['Details']['Experimental']))
        #     docker_file.write("\t\tOS: {}\n".format(components['Details']['Os'] ))
        #     docker_file.write("\t\tMinAPIVersion {}\n".format(components['Details']['MinAPIVersion']))
        #     docker_file.write("\t\tKernelVersion: {}\n".format(components['Details']['KernelVersion']))
        #     docker_file.write("\t\tGoVersion: {}\n".format(components['Details']['GoVersion'] ))
        #     docker_file.write("\t\tGitCommit: {}\n".format(components['Details']['GitCommit'] ))
        #     docker_file.write("\t\tBuildTime: {}\n".format(components['Details']['BuildTime'] ))
        #     docker_file.write("\t\tApiVersion: {}\n".format(components['Details']['ApiVersion']))
        #     docker_file.write("\t\tArch: {}\n".format(components['Details']['Arch']))
    docker_file.close()
