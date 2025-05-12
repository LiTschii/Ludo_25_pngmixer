#!/usr/bin/env python3
"""
PNG Mixer CLI - Creates duplex-ready PNG files with A-type and B-type images
on separate pages for double-sided printing.

Enhanced version with duplex printing support.
"""

import click
import random
import os
import sys
from pathlib import Path
from PIL import Image
import json

class PNGMixerCLI:
    def __init__(self):
        # DIN A4 dimensions at 300 DPI: 2480 x 3508 pixels
        self.output_width = 2480
        self.output_height = 3508
        self.images_per_row = 6
        
        # Image storage
        self.loaded_a_images = {}
        self.loaded_b_images = {}
        
        # Extended configuration with all paths
        self.config = {
            # Image paths
            'paths': {
                'a_common': '',
                'a_uncommon': '',
                'a_legendary': '',
                'b_normal': '',
                'b_special': ''
            },
            # Distribution settings
            'distribution': {
                'a_common': 70,
                'a_uncommon': 25,
                'a_legendary': 5,
                'b_special': 10
            },
            # Output settings
            'output': {
                'filename': 'ludo_mixed_output.png',
                'width': 2480,
                'height': 3508,
                'images_per_row': 6,
                'duplex_mode': True  # New: separate A and B pages
            }
        }
        
    def validate_image(self, filepath, expected_size=(500, 500)):
        """Validate if image exists and has correct format"""
        if not filepath or not os.path.exists(filepath):
            return False, f"File not found: {filepath}"
            
        try:
            with Image.open(filepath) as img:
                if img.format.upper() != 'PNG':
                    return False, f"File must be PNG format, but is {img.format}"
                if img.size != expected_size:
                    click.echo(f"Warning: Image {filepath} is {img.size}, will be resized to {expected_size}")
                return True, "Valid image"
        except Exception as e:
            return False, f"Error reading image: {str(e)}"
    
    def load_image(self, filepath, resize_to=(500, 500)):
        """Load and resize image if necessary"""
        try:
            img = Image.open(filepath)
            if img.size != resize_to:
                img = img.resize(resize_to, Image.Resampling.LANCZOS)
            return img
        except Exception as e:
            raise click.ClickException(f"Failed to load image {filepath}: {str(e)}")
    
    def save_config(self, config_file="png_mixer_config.json"):
        """Save current configuration to JSON file"""
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        click.echo(f"Configuration saved to {config_file}")
    
    def load_config(self, config_file="png_mixer_config.json"):
        """Load configuration from JSON file"""
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                loaded_config = json.load(f)
                # Handle both old and new config format
                if 'paths' in loaded_config:
                    self.config.update(loaded_config)
                else:
                    # Old format - migrate to new format
                    if 'a_common' in loaded_config:
                        self.config['distribution'].update({
                            'a_common': loaded_config.get('a_common', 70),
                            'a_uncommon': loaded_config.get('a_uncommon', 25),
                            'a_legendary': loaded_config.get('a_legendary', 5),
                            'b_special': loaded_config.get('b_special', 10)
                        })
            click.echo(f"Configuration loaded from {config_file}")
            return True
        return False
    
    def load_images_from_config(self):
        """Load all images based on configuration paths"""
        paths = self.config['paths']
        
        # Check if all required paths are set
        missing_paths = [key for key, path in paths.items() if not path]
        if missing_paths:
            raise click.ClickException(f"Missing paths in config: {', '.join(missing_paths)}")
        
        # Validate and load A-type images
        for rarity, path_key in [('common', 'a_common'), ('uncommon', 'a_uncommon'), ('legendary', 'a_legendary')]:
            path = paths[path_key]
            valid, msg = self.validate_image(path)
            if not valid:
                raise click.ClickException(f"A-type {rarity}: {msg}")
            self.loaded_a_images[rarity] = self.load_image(path)
            click.echo(f"  ✅ A-type {rarity}: {path}")
        
        # Validate and load B-type images
        for variant, path_key in [('normal', 'b_normal'), ('special', 'b_special')]:
            path = paths[path_key]
            valid, msg = self.validate_image(path)
            if not valid:
                raise click.ClickException(f"B-type {variant}: {msg}")
            self.loaded_b_images[variant] = self.load_image(path)
            click.echo(f"  ✅ B-type {variant}: {path}")
    
    def create_page(self, images, page_type="A"):
        """Create a single page with given images"""
        # Calculate image layout
        img_width = 500
        img_height = 500
        scale_factor = self.output_width / (self.images_per_row * img_width)
        scaled_width = int(img_width * scale_factor)
        scaled_height = int(img_height * scale_factor)
        
        rows_possible = self.output_height // scaled_height
        total_slots = self.images_per_row * rows_possible
        
        # Create the page
        page_img = Image.new('RGB', (self.output_width, self.output_height), 'white')
        
        # Place images
        for i, img in enumerate(images):
            if i >= total_slots:
                break
                
            row = i // self.images_per_row
            col = i % self.images_per_row
            
            x = col * scaled_width
            y = row * scaled_height
            
            # Scale the image
            scaled_img = img.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
            page_img.paste(scaled_img, (x, y))
        
        return page_img, len(images), total_slots
    
    def generate_duplex_images(self, output_path=None):
        """Generate separate A and B pages for duplex printing"""
        if output_path is None:
            output_path = self.config['output']['filename']
            
        # Get distribution settings
        dist = self.config['distribution']
        
        # Normalize A-type probabilities
        total_a = dist['a_common'] + dist['a_uncommon'] + dist['a_legendary']
        if total_a == 0:
            raise click.ClickException("A-type probabilities cannot all be zero!")
            
        a_probs = {
            'common': dist['a_common'] / total_a,
            'uncommon': dist['a_uncommon'] / total_a,
            'legendary': dist['a_legendary'] / total_a
        }
        
        # B-type probability
        b_special_prob = dist['b_special'] / 100
        
        # Calculate how many images we need
        img_width = 500
        img_height = 500
        scale_factor = self.output_width / (self.images_per_row * img_width)
        scaled_height = int(img_height * scale_factor)
        rows_possible = self.output_height // scaled_height
        total_slots = self.images_per_row * rows_possible
        
        click.echo(f"Generating {total_slots} images per page")
        
        # Generate A-type images
        click.echo("🎯 Generating A-type images...")
        a_images = []
        for i in range(total_slots):
            rand = random.random()
            if rand < a_probs['common']:
                a_images.append(self.loaded_a_images['common'])
            elif rand < a_probs['common'] + a_probs['uncommon']:
                a_images.append(self.loaded_a_images['uncommon'])
            else:
                a_images.append(self.loaded_a_images['legendary'])
        
        # Generate B-type images
        click.echo("🎯 Generating B-type images...")
        b_images = []
        for i in range(total_slots):
            if random.random() < b_special_prob:
                b_images.append(self.loaded_b_images['special'])
            else:
                b_images.append(self.loaded_b_images['normal'])
        
        # Create pages
        click.echo("📄 Creating A-type page...")
        page_a, a_count, a_slots = self.create_page(a_images, "A")
        
        click.echo("📄 Creating B-type page...")
        # For duplex compatibility, we need to mirror B page horizontally
        page_b, b_count, b_slots = self.create_page(b_images, "B")
        page_b = page_b.transpose(Image.FLIP_LEFT_RIGHT)  # Mirror for duplex
        
        # Generate output filenames
        base_name = os.path.splitext(output_path)[0]
        page_a_path = f"{base_name}_page_A.png"
        page_b_path = f"{base_name}_page_B.png"
        
        # Save pages
        page_a.save(page_a_path)
        page_b.save(page_b_path)
        
        click.echo(f"\n✅ Pages saved successfully!")
        click.echo(f"  📄 A-type page: {page_a_path}")
        click.echo(f"  📄 B-type page: {page_b_path} (mirrored for duplex)")
        
        # Show statistics
        click.echo("\n📊 Generation Statistics:")
        click.echo(f"  🎯 A-type page: {a_count} images ({total_slots} slots)")
        click.echo(f"    • Common: {a_probs['common']*100:.1f}% chance")
        click.echo(f"    • Uncommon: {a_probs['uncommon']*100:.1f}% chance")  
        click.echo(f"    • Legendary: {a_probs['legendary']*100:.1f}% chance")
        click.echo(f"  🎯 B-type page: {b_count} images ({total_slots} slots)")
        click.echo(f"    • Special chance: {b_special_prob*100:.1f}%")
        
        click.echo("\n🖨️ Duplex Printing Instructions:")
        click.echo("  1. Print page A first")
        click.echo("  2. Put printed page back in printer (flipped)")
        click.echo("  3. Print page B")
        click.echo("  4. Pages should align perfectly!")
        
        return page_a_path, page_b_path

    def generate_mixed_image(self, output_path=None):
        """Generate images - duplex mode or traditional mode based on config"""
        if self.config['output'].get('duplex_mode', True):
            return self.generate_duplex_images(output_path)
        else:
            # Fallback to old mixed mode (not recommended)
            click.echo("⚠️ Warning: Mixed mode is deprecated. Using duplex mode.")
            return self.generate_duplex_images(output_path)


# CLI Interface
@click.group()
@click.pass_context
def cli(ctx):
    """🎮 Ludo PNG Mixer - Generate duplex-ready A and B type PNG images"""
    ctx.ensure_object(dict)
    ctx.obj['mixer'] = PNGMixerCLI()


@cli.command()
@click.pass_context
def interactive(ctx):
    """🔄 Interactive mode - guided setup and configuration"""
    mixer = ctx.obj['mixer']
    
    click.echo("🎮 Welcome to Ludo PNG Mixer - Duplex Mode")
    click.echo("=" * 50)
    
    # Load existing config if available
    if mixer.load_config():
        click.echo("📋 Current configuration loaded!")
    
    # Image loading section
    click.echo("\n📁 Image Loading Section")
    click.echo("-" * 30)
    
    # A-type images
    click.echo("\n🎯 A-Type Images (3 rarity levels):")
    for rarity, config_key, default_filename in [
        ('common', 'a_common', 'a.png'), 
        ('uncommon', 'a_uncommon', 'b.png'), 
        ('legendary', 'a_legendary', 'c.png')
    ]:
        while True:
            current_path = mixer.config['paths'][config_key]
            default_path = current_path or (default_filename if os.path.exists(default_filename) else "")
            path = click.prompt(f"  Path to {rarity} image", default=default_path, show_default=bool(default_path))
            
            if not path:
                continue
                
            valid, msg = mixer.validate_image(path)
            if valid:
                mixer.config['paths'][config_key] = path
                mixer.loaded_a_images[rarity] = mixer.load_image(path)
                click.echo(f"  ✅ {rarity.capitalize()} image loaded!")
                break
            else:
                click.echo(f"  ❌ {msg}")
    
    # B-type images  
    click.echo("\n🎯 B-Type Images (2 variants):")
    for variant, config_key, default_filename in [
        ('normal', 'b_normal', 'xp.png'), 
        ('special', 'b_special', 'xpxd.png')
    ]:
        while True:
            current_path = mixer.config['paths'][config_key]
            default_path = current_path or (default_filename if os.path.exists(default_filename) else "")
            path = click.prompt(f"  Path to {variant} image", default=default_path, show_default=bool(default_path))
            
            if not path:
                continue
                
            valid, msg = mixer.validate_image(path)
            if valid:
                mixer.config['paths'][config_key] = path
                mixer.loaded_b_images[variant] = mixer.load_image(path)
                click.echo(f"  ✅ {variant.capitalize()} image loaded!")
                break
            else:
                click.echo(f"  ❌ {msg}")
    
    # Configuration section
    click.echo("\n⚙️  Configuration Section")
    click.echo("-" * 30)
    
    dist = mixer.config['distribution']
    click.echo("\nA-Type Distribution (percentages):")
    dist['a_common'] = click.prompt("  Common %", type=int, default=dist['a_common'])
    dist['a_uncommon'] = click.prompt("  Uncommon %", type=int, default=dist['a_uncommon'])
    dist['a_legendary'] = click.prompt("  Legendary %", type=int, default=dist['a_legendary'])
    
    click.echo("\nB-Type Configuration:")
    dist['b_special'] = click.prompt("  Special chance %", type=int, default=dist['b_special'])
    
    # Output configuration
    click.echo("\nOutput Configuration:")
    output_config = mixer.config['output']
    output_config['filename'] = click.prompt("  Base output filename", default=output_config['filename'])
    
    # Save configuration
    if click.confirm("\n💾 Save this configuration for future use?", default=True):
        mixer.save_config()
    
    # Generate image
    click.echo("\n🎨 Generating Duplex Pages")
    click.echo("-" * 30)
    
    try:
        page_a_path, page_b_path = mixer.generate_mixed_image()
        if click.confirm("\n🚀 Open the output folder?", default=True):
            output_dir = os.path.dirname(os.path.abspath(page_a_path)) or "."
            # Use WSL-compatible command
            os.system(f'explorer.exe "{output_dir}"')
    except Exception as e:
        click.echo(f"\n❌ Error generating images: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option('--config', '-c', type=str, default='png_mixer_config.json', help='Configuration file to use')
@click.pass_context
def generate(ctx, config):
    """🎨 Generate duplex images from configuration file"""
    mixer = ctx.obj['mixer']
    
    if not os.path.exists(config):
        raise click.ClickException(f"Configuration file not found: {config}")
    
    # Load configuration
    click.echo(f"📋 Loading configuration from {config}")
    mixer.load_config(config)
    
    # Check if all paths are set
    paths = mixer.config['paths']
    missing_paths = [key for key, path in paths.items() if not path]
    if missing_paths:
        raise click.ClickException(f"Missing paths in config: {', '.join(missing_paths)}")
    
    # Validate and load images
    click.echo("🔍 Validating and loading images...")
    try:
        mixer.load_images_from_config()
    except Exception as e:
        raise click.ClickException(str(e))
    
    # Generate images
    click.echo("\n🎨 Generating duplex pages...")
    try:
        page_a_path, page_b_path = mixer.generate_mixed_image()
    except Exception as e:
        raise click.ClickException(f"Failed to generate images: {str(e)}")


@cli.command()
@click.option('--config', '-c', type=str, default='png_mixer_config.json', help='Configuration file path')
@click.pass_context 
def config(ctx, config):
    """⚙️ Manage configuration settings"""
    mixer = ctx.obj['mixer']
    
    if not os.path.exists(config):
        click.echo(f"📄 Creating new configuration file: {config}")
        mixer.save_config(config)
    else:
        mixer.load_config(config)
        click.echo(f"📄 Current configuration from {config}:")
        click.echo(f"\nImage Paths:")
        for key, path in mixer.config['paths'].items():
            click.echo(f"  {key}: {path or 'Not set'}")
        click.echo(f"\nDistribution:")
        dist = mixer.config['distribution']
        click.echo(f"  A-Type - Common: {dist['a_common']}%, Uncommon: {dist['a_uncommon']}%, Legendary: {dist['a_legendary']}%")
        click.echo(f"  B-Type Special Chance: {dist['b_special']}%")
        click.echo(f"\nOutput:")
        output = mixer.config['output']
        click.echo(f"  Base filename: {output['filename']}")
        click.echo(f"  Size: {output['width']}x{output['height']}")
        click.echo(f"  Images per row: {output['images_per_row']}")
        click.echo(f"  Duplex mode: {'Enabled' if output.get('duplex_mode', True) else 'Disabled'}")


@cli.command()
def examples():
    """📚 Show usage examples for duplex mode"""
    click.echo("🎮 Ludo PNG Mixer - Duplex Mode Examples")
    click.echo("=" * 40)
    
    click.echo("\n1️⃣  Interactive Setup (Recommended):")
    click.echo("   ./cli.sh interactive")
    click.echo("   # Creates page_A.png and page_B.png")
    
    click.echo("\n2️⃣  Generate from configuration:")
    click.echo("   ./cli.sh generate")
    click.echo("   # Outputs: filename_page_A.png and filename_page_B.png")
    
    click.echo("\n3️⃣  Duplex Printing Process:")
    click.echo("   📄 1. Print page_A.png")
    click.echo("   🔄 2. Flip the paper and put it back")
    click.echo("   📄 3. Print page_B.png")
    click.echo("   ✅ 4. Images should align perfectly!")
    
    click.echo("\n4️⃣  Configuration example:")
    example_config = {
        "paths": {
            "a_common": "cards/a_common.png",
            "a_uncommon": "cards/a_uncommon.png",
            "a_legendary": "cards/a_legendary.png",
            "b_normal": "cards/b_normal.png",
            "b_special": "cards/b_special.png"
        },
        "distribution": {
            "a_common": 70,
            "a_uncommon": 25,
            "a_legendary": 5,
            "b_special": 10
        },
        "output": {
            "filename": "ludo_cards.png",
            "width": 2480,
            "height": 3508,
            "images_per_row": 6,
            "duplex_mode": True
        }
    }
    click.echo(json.dumps(example_config, indent=2))
    
    click.echo("\n💡 Tips:")
    click.echo("   • Page B is automatically mirrored for duplex compatibility")
    click.echo("   • Use high-quality 300 DPI settings on your printer")
    click.echo("   • Always test with a single page first")
    click.echo("   • Both pages will have the same number of images")


# Keep the batch command for backwards compatibility
@cli.command()
@click.option('--common', type=str, help='Path to common A-type image (a.png)')
@click.option('--uncommon', type=str, help='Path to uncommon A-type image (b.png)')
@click.option('--legendary', type=str, help='Path to legendary A-type image (c.png)')
@click.option('--normal', type=str, help='Path to normal B-type image (xp.png)')
@click.option('--special', type=str, help='Path to special B-type image (xpxd.png)')
@click.option('--a-common', type=int, help='Common A-type percentage')
@click.option('--a-uncommon', type=int, help='Uncommon A-type percentage')
@click.option('--a-legendary', type=int, help='Legendary A-type percentage')
@click.option('--b-special', type=int, help='B-type special chance percentage')
@click.option('--output', '-o', type=str, help='Output filename')
@click.option('--config', type=str, help='Save/load configuration from JSON file')
@click.pass_context
def batch(ctx, **kwargs):
    """⚡ Batch mode - quick setup with command-line options (DEPRECATED)"""
    click.echo("⚠️  Warning: 'batch' command is deprecated!")
    click.echo("   The new version creates separate A and B pages for duplex printing.")
    click.echo("   Use 'interactive' mode to set up your config, then use 'generate'.")
    click.echo("\n   Recommended workflow:")
    click.echo("   1. ./cli.sh interactive     # Set up configuration")
    click.echo("   2. ./cli.sh generate        # Generate duplex-ready pages")
    
    # Still support batch mode but convert to duplex
    mixer = ctx.obj['mixer']
    
    # Load config if specified
    if kwargs['config'] and os.path.exists(kwargs['config']):
        mixer.load_config(kwargs['config'])
    
    # Update configuration from command line args (only if provided)
    if kwargs.get('a_common') is not None:
        mixer.config['distribution']['a_common'] = kwargs['a_common']
    if kwargs.get('a_uncommon') is not None:
        mixer.config['distribution']['a_uncommon'] = kwargs['a_uncommon']
    if kwargs.get('a_legendary') is not None:
        mixer.config['distribution']['a_legendary'] = kwargs['a_legendary']
    if kwargs.get('b_special') is not None:
        mixer.config['distribution']['b_special'] = kwargs['b_special']
    
    # Required image paths
    required_args = ['common', 'uncommon', 'legendary', 'normal', 'special']
    missing_args = [arg for arg in required_args if not kwargs.get(arg)]
    if missing_args:
        raise click.ClickException(f"Missing required arguments: {', '.join(f'--{arg}' for arg in missing_args)}")
    
    # Set image paths
    mixer.config['paths']['a_common'] = kwargs['common']
    mixer.config['paths']['a_uncommon'] = kwargs['uncommon']
    mixer.config['paths']['a_legendary'] = kwargs['legendary']
    mixer.config['paths']['b_normal'] = kwargs['normal']
    mixer.config['paths']['b_special'] = kwargs['special']
    
    # Set output path if provided
    if kwargs.get('output'):
        mixer.config['output']['filename'] = kwargs['output']
    
    # Validate and load images
    click.echo("🔍 Validating images...")
    try:
        mixer.load_images_from_config()
    except Exception as e:
        raise click.ClickException(str(e))
    
    # Save config if specified
    if kwargs['config']:
        mixer.save_config(kwargs['config'])
    
    # Generate duplex images instead of mixed
    click.echo("\n🎨 Generating duplex pages...")
    try:
        page_a_path, page_b_path = mixer.generate_mixed_image()
    except Exception as e:
        raise click.ClickException(f"Failed to generate images: {str(e)}")


if __name__ == '__main__':
    cli()
