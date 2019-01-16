import boto3
import click

session = boto3.Session(profile_name='anup')
ec2 = session.resource('ec2')


@click.group()
def cli():
    """ Commands for instances and snapshots """


@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('stop')
@click.option('--project', default=None, help="Only stop instances for project (tag Project:<name>)")
def stop_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project','Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        print("Stopping {0}..".format(i.id))
        i.stop()
        i.wait_until_stopped()
        print("Stopped {0}..".format(i.id))


@instances.command('list')
@click.option('--project', default=None, help="Only show instances for project (tag Project:<name>)")
def list_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        print("ID:{0}  State:{1}".format(i.id,i.state))


@instances.command('start')
@click.option('--project', default=None,help="Only start instances for project (tag Project:<name>)")
def start_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()


    for i in instances:
        print("Starting {0}..".format(i.id))
        i.start()


@cli.group('volumes')
def volumes():
    """ Commands for volumes """


@volumes.command('list')
@click.option('--project', default=None, help="Only list volumes for project (tag Project:<name>)")
def list_volumes(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        for v in i.volumes.all():            
            print("Instance {0} - Volume {1}".format(i.id, v.id))   

    return

@cli.group('snapshots')
def snapshots():
    """ Commands for snapshots """

@snapshots.command('list')
@click.option('--project', default=None, help="Only list snapshots for project (tag Project:<name>)")
def list_snapshots(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        print("-Instance ID: {0}".format(i.id))
        for v in i.volumes.all(): 
            print("--Volume ID: {0}".format(i.id))
            for s in v.snapshots.all():
                print("---Snapshot ID:{0} State: {1}".format(s.id,s.state))

@snapshots.command('create')
@click.option('--project', default=None, help="Only create snapshots for project (tag Project:<name>)")
def create_snapshots(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        print("Stopping instance with ID: {0}".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all(): 
             print("Creating snapshot for :{0} ".format(v.id))
             v.create_snapshot(Description="Created by boto3 API")        
        print("Starting instance with ID: {0}".format(i.id))
        i.start()
        i.wait_until_running()

if __name__ == '__main__':
    cli()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     