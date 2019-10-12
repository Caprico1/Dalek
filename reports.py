import os

def get_all_reports():
    #cat out each directory
    reports = os.listdir("reports")

    print("\nREPORTS: \n")
    for i in range(len(reports)):
        print("{0} : {1}".format(i+1, reports[i]))

    #User selects Report/scan
    select_report = input("\nSelect a report (Numbers Only): ")

    report_dir = reports[int(select_report)-1]


    #cat out each IP.txt. Pagination might Be required.
    result_files = [f for f in os.listdir("reports/{0}".format(report_dir)) if os.path.isfile(os.path.join("reports/{0}".format(report_dir), f))]
    ip = ""
    for i in range(len(result_files)):
        print("{0} : {1}".format(i+1, result_files[i]))

        if i % 10 == 0:
            ip_selection = input("Next: [N] Previous: [P] Select: [Enter Number]: ")
            if ip_selection.upper() == "N":
                continue
            # if ip_selection.upper() == "P":
            #     i -= 10
            #     continue
            else:
                #user selects IP
                ip = result_files[int(ip_selection)-1][:-4]
                break

    #Return ip to monitor.
    return ip
