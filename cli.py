import click
import json
from ace_driver import ACEDriver


@click.group()
def cli():
    """A command-line interface for the ValgACE device."""
    pass


@cli.command()
def status():
    """Get the status of the ACE device."""
    driver = ACEDriver()
    try:
        driver.connect()
        device_status = driver.get_status()
        print(json.dumps(device_status, indent=2))
    finally:
        driver.disconnect()


@cli.command()
@click.argument('slot', type=int)
def filament_info(slot):
    """Get filament information for a specific slot."""
    driver = ACEDriver()
    try:
        driver.connect()
        filament_info = driver.get_filament_info(slot)
        print(json.dumps(filament_info, indent=2))
    finally:
        driver.disconnect()


@cli.command()
@click.argument('slot', type=int)
def park_to_toolhead(slot):
    """Park to toolhead."""
    driver = ACEDriver()
    try:
        driver.connect()
        result = driver.park_to_toolhead(slot)
        print(json.dumps(result, indent=2))
    finally:
        driver.disconnect()


@cli.command()
@click.argument('slot', type=int)
@click.argument('length', type=float)
@click.argument('speed', type=int)
def feed(slot, length, speed):
    """Feed filament."""
    driver = ACEDriver()
    try:
        driver.connect()
        result = driver.feed(slot, length, speed)
        print(json.dumps(result, indent=2))
    finally:
        driver.disconnect()


@cli.command()
@click.argument('slot', type=int)
@click.argument('length', type=float)
@click.argument('speed', type=int)
def retract(slot, length, speed):
    """Retract filament."""
    driver = ACEDriver()
    try:
        driver.connect()
        result = driver.retract(slot, length, speed)
        print(json.dumps(result, indent=2))
    finally:
        driver.disconnect()


@cli.command()
@click.argument('slot', type=int)
def stop_feed(slot):
    """Stop feeding filament."""
    driver = ACEDriver()
    try:
        driver.connect()
        result = driver.stop_feed(slot)
        print(json.dumps(result, indent=2))
    finally:
        driver.disconnect()


@cli.command()
@click.argument('slot', type=int)
def stop_retract(slot):
    """Stop retracting filament."""
    driver = ACEDriver()
    try:
        driver.connect()
        result = driver.stop_retract(slot)
        print(json.dumps(result, indent=2))
    finally:
        driver.disconnect()


@cli.command()
@click.argument('slot', type=int)
@click.argument('speed', type=int)
def update_feed_speed(slot, speed):
    """Update feed speed."""
    driver = ACEDriver()
    try:
        driver.connect()
        result = driver.update_feed_speed(slot, speed)
        print(json.dumps(result, indent=2))
    finally:
        driver.disconnect()


@cli.command()
@click.argument('slot', type=int)
@click.argument('speed', type=int)
def update_retract_speed(slot, speed):
    """Update retract speed."""
    driver = ACEDriver()
    try:
        driver.connect()
        result = driver.update_retract_speed(slot, speed)
        print(json.dumps(result, indent=2))
    finally:
        driver.disconnect()


@cli.command()
@click.argument('slot', type=int)
def enable_feed_assist(slot):
    """Enable feed assist."""
    driver = ACEDriver()
    try:
        driver.connect()
        result = driver.enable_feed_assist(slot)
        print(json.dumps(result, indent=2))
    finally:
        driver.disconnect()


@cli.command()
@click.argument('slot', type=int)
def disable_feed_assist(slot):
    """Disable feed assist."""
    driver = ACEDriver()
    try:
        driver.connect()
        result = driver.disable_feed_assist(slot)
        print(json.dumps(result, indent=2))
    finally:
        driver.disconnect()


@cli.command()
@click.argument('temp', type=int)
@click.argument('duration', type=int)
def start_drying(temp, duration):
    """Start filament drying."""
    driver = ACEDriver()
    try:
        driver.connect()
        result = driver.start_drying(temp, duration)
        print(json.dumps(result, indent=2))
    finally:
        driver.disconnect()


@cli.command()
def stop_drying():
    """Stop filament drying."""
    driver = ACEDriver()
    try:
        driver.connect()
        result = driver.stop_drying()
        print(json.dumps(result, indent=2))
    finally:
        driver.disconnect()


@cli.command()
@click.argument('command_string')
def debug_send(command_string):
    """Send a raw command for debugging purposes."""
    driver = ACEDriver()
    try:
        driver.connect()
        result = driver.debug_send(command_string)
        print(json.dumps(result, indent=2))
    finally:
        driver.disconnect()