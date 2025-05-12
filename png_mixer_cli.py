#!/usr/bin/env python3
"""
PNG Mixer CLI - Creates a DIN A4 format PNG from A-type and B-type images
with configurable rarity distribution.

Command-line version optimized for WSL/headless environments.
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
        
        # Configuration
        self.config = {
            'a_common': 70,
            'a_uncommon': 25,
            'a_legendary': 5,
            'b_special': 10
        }
        
    def validate_image(self, filepath, expected_size=(500, 500)):
        """Validate if image exists and has correct format"""
        if not os.path.exists(filepath):
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
                self.config.update(json.load(f))
            click.echo(f"Configuration loaded from {config_file}")
            return True
        return False
    
    def generate_mixed_image(self, output_path="mixed_output.png"):
        """Generate the mixed PNG image"""
        # Normalize A-type probabilities
        total_a = self.config['a_common'] + self.config['a_uncommon'] + self.config['a_legendary']
        if total_a == 0:
            raise click.ClickException("A-type probabilities cannot all be zero!")
            
        a_probs = {
            'common': self.config['a_common'] / total_a,
            'uncommon': self.config['a_uncommon'] / total_a,
            'legendary': self.config['a_legendary'] / total_a
        }
        
        # B-type probability
        b_special_prob = self.config['b_special'] / 100
        
        # Calculate image layout
        img_width = 500
        img_height = 500
        scale_factor = self.output_width / (self.images_per_row * img_width)
        scaled_width = int(img_width * scale_factor)
        scaled_height = int(img_height * scale_factor)
        
        rows_possible = self.output_height // scaled_height
        total_images = self.images_per_row * rows_possible
        
        # Ensure A:B ratio is 1:1
        a_count = total_images // 2
        b_count = total_images - a_count
        
        click.echo(f"Generating image with {total_images} images ({a_count} A-type, {b_count} B-type)")
        
        # Generate A-type image list
        a_images = []
        for _ in range(a_count):
            rand = random.random()
            if rand < a_probs['common']:
                a_images.append(self.loaded_a_images['common'])
            elif rand < a_probs['common'] + a_probs['uncommon']:
                a_images.append(self.loaded_a_images['uncommon'])
            else:
                a_images.append(self.loaded_a_images['legendary'])
        
        # Generate B-type image list
        b_images = []
        for _ in range(b_count):
            if random.random() < b_special_prob:
                b_images.append(self.loaded_b_images['special'])
            else:
                b_images.append(self.loaded_b_images['normal'])
        
        # Combine and shuffle
        all_images = a_images + b_images
        random.shuffle(all_images)
        
        # Create the output image
        output_img = Image.new('RGB', (self.output_width, self.output_height), 'white')
        
        # Place images with progress
        with click.progressbar(enumerate(all_images), length=len(all_images), 
                              label="Placing images") as items:
            for i, img in items:
                if i >= total_images:
                    break
                    
                row = i // self.images_per_row
                col = i % self.images_per_row
                
                x = col * scaled_width
                y = row * scaled_height
                
                # Scale the image
                scaled_img = img.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
                output_img.paste(scaled_img, (x, y))
        
        # Save the image
        output_img.save(output_path)
        click.echo(f"\n✅ Image saved successfully to {output_path}")
        
        # Show statistics
        click.echo("\n📊 Generation Statistics:")
        click.echo(f"  Total images: {total_images}")
        click.echo(f"  A-type: {a_count} (Common: {a_probs['common']*100:.1f}%, "
                  f"Uncommon: {a_probs['uncommon']*100:.1f}%, "
                  f"Legendary: {a_probs['legendary']*100:.1f}%)")
        click.echo(f"  B-type: {b_count} (Special chance: {b_special_prob*100:.1f}%)")


# CLI Interface
@click.group()
@click.pass_context
def cli(ctx):
    """🎮 Ludo PNG Mixer - Mix A-type and B-type PNG images"""
    ctx.ensure_object(dict)
    ctx.obj['mixer'] = PNGMixerCLI()


@cli.command()
@click.pass_context
def interactive(ctx):
    """🔄 Interactive mode - guided setup and configuration"""
    mixer = ctx.obj['mixer']
    
    click.echo("🎮 Welcome to Ludo PNG Mixer - Interactive Mode")
    click.echo("=" * 50)
    
    # Load existing config if available
    if mixer.load_config():
        click.echo("📋 Current configuration loaded!")
    
    # Image loading section
    click.echo("\n📁 Image Loading Section")
    click.echo("-" * 30)
    
    # A-type images
    click.echo("\n🎯 A-Type Images (3 rarity levels):")
    for rarity, filename in [('common', 'a.png'), ('uncommon', 'b.png'), ('legendary', 'c.png')]:
        while True:
            default_path = filename if os.path.exists(filename) else ""
            path = click.prompt(f"  Path to {rarity} image", default=default_path, show_default=bool(default_path))
            
            if not path:
                continue
                
            valid, msg = mixer.validate_image(path)
            if valid:
                mixer.loaded_a_images[rarity] = mixer.load_image(path)
                click.echo(f"  ✅ {rarity.capitalize()} image loaded!")
                break
            else:
                click.echo(f"  ❌ {msg}")
    
    # B-type images  
    click.echo("\n🎯 B-Type Images (2 variants):")
    for variant, filename in [('normal', 'xp.png'), ('special', 'xpxd.png')]:
        while True:
            default_path = filename if os.path.exists(filename) else ""
            path = click.prompt(f"  Path to {variant} image", default=default_path, show_default=bool(default_path))
            
            if not path:
                continue
                
            valid, msg = mixer.validate_image(path)
            if valid:
                mixer.loaded_b_images[variant] = mixer.load_image(path)
                click.echo(f"  ✅ {variant.capitalize()} image loaded!")
                break
            else:
                click.echo(f"  ❌ {msg}")
    
    # Configuration section
    click.echo("\n⚙️  Configuration Section")
    click.echo("-" * 30)
    
    click.echo("\nA-Type Distribution (percentages):")
    mixer.config['a_common'] = click.prompt("  Common %", type=int, default=mixer.config['a_common'])
    mixer.config['a_uncommon'] = click.prompt("  Uncommon %", type=int, default=mixer.config['a_uncommon'])
    mixer.config['a_legendary'] = click.prompt("  Legendary %", type=int, default=mixer.config['a_legendary'])
    
    click.echo("\nB-Type Configuration:")
    mixer.config['b_special'] = click.prompt("  Special chance %", type=int, default=mixer.config['b_special'])
    
    # Save configuration
    if click.confirm("\n💾 Save this configuration for future use?", default=True):
        mixer.save_config()
    
    # Generate image
    click.echo("\n🎨 Generating Mixed Image")
    click.echo("-" * 30)
    
    default_output = "ludo_mixed_output.png"
    output_path = click.prompt("Output filename", default=default_output, show_default=True)
    
    try:
        mixer.generate_mixed_image(output_path)
        if click.confirm("\n🚀 Open the output folder?", default=True):
            output_dir = os.path.dirname(os.path.abspath(output_path)) or "."
            click.launch(output_dir)
    except Exception as e:
        click.echo(f"\n❌ Error generating image: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option('--common', type=str, required=True, help='Path to common A-type image (a.png)')
@click.option('--uncommon', type=str, required=True, help='Path to uncommon A-type image (b.png)')
@click.option('--legendary', type=str, required=True, help='Path to legendary A-type image (c.png)')
@click.option('--normal', type=str, required=True, help='Path to normal B-type image (xp.png)')
@click.option('--special', type=str, required=True, help='Path to special B-type image (xpxd.png)')
@click.option('--a-common', type=int, default=70, help='Common A-type percentage')
@click.option('--a-uncommon', type=int, default=25, help='Uncommon A-type percentage')
@click.option('--a-legendary', type=int, default=5, help='Legendary A-type percentage')
@click.option('--b-special', type=int, default=10, help='B-type special chance percentage')
@click.option('--output', '-o', type=str, default='ludo_mixed_output.png', help='Output filename')
@click.option('--config', type=str, help='Load/save configuration from JSON file')
@click.pass_context
def batch(ctx, **kwargs):
    """⚡ Batch mode - quick generation with command-line options"""
    mixer = ctx.obj['mixer']
    
    # Load config if specified
    if kwargs['config'] and os.path.exists(kwargs['config']):
        mixer.load_config(kwargs['config'])
    
    # Update configuration
    mixer.config.update({
        'a_common': kwargs['a_common'],
        'a_uncommon': kwargs['a_uncommon'],
        'a_legendary': kwargs['a_legendary'],
        'b_special': kwargs['b_special']
    })
    
    # Validate and load images
    image_paths = {
        'a': {
            'common': kwargs['common'],
            'uncommon': kwargs['uncommon'],
            'legendary': kwargs['legendary']
        },
        'b': {
            'normal': kwargs['normal'],
            'special': kwargs['special']
        }
    }
    
    click.echo("🔍 Validating images...")
    
    # Load A-type images
    for rarity, path in image_paths['a'].items():
        valid, msg = mixer.validate_image(path)
        if not valid:
            raise click.ClickException(f"A-type {rarity}: {msg}")
        mixer.loaded_a_images[rarity] = mixer.load_image(path)
        click.echo(f"  ✅ A-type {rarity}: {path}")
    
    # Load B-type images
    for variant, path in image_paths['b'].items():
        valid, msg = mixer.validate_image(path)
        if not valid:
            raise click.ClickException(f"B-type {variant}: {msg}")
        mixer.loaded_b_images[variant] = mixer.load_image(path)
        click.echo(f"  ✅ B-type {variant}: {path}")
    
    # Save config if specified
    if kwargs['config']:
        mixer.save_config(kwargs['config'])
    
    # Generate image
    click.echo("\n🎨 Generating mixed image...")
    try:
        mixer.generate_mixed_image(kwargs['output'])
    except Exception as e:
        raise click.ClickException(f"Failed to generate image: {str(e)}")


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
        click.echo(f"  A-Type Distribution:")
        click.echo(f"    Common: {mixer.config['a_common']}%")
        click.echo(f"    Uncommon: {mixer.config['a_uncommon']}%")
        click.echo(f"    Legendary: {mixer.config['a_legendary']}%")
        click.echo(f"  B-Type Special Chance: {mixer.config['b_special']}%")


@cli.command()
def examples():
    """📚 Show usage examples"""
    click.echo("🎮 Ludo PNG Mixer - Usage Examples")
    click.echo("=" * 40)
    
    click.echo("\n1️⃣  Interactive Mode (Recommended):")
    click.echo("   python png_mixer_cli.py interactive")
    
    click.echo("\n2️⃣  Batch Mode with all options:")
    click.echo("   python png_mixer_cli.py batch \\")
    click.echo("     --common a.png \\")
    click.echo("     --uncommon b.png \\") 
    click.echo("     --legendary c.png \\")
    click.echo("     --normal xp.png \\")
    click.echo("     --special xpxd.png \\")
    click.echo("     --a-common 60 \\")
    click.echo("     --a-uncommon 30 \\")
    click.echo("     --a-legendary 10 \\")
    click.echo("     --b-special 15 \\")
    click.echo("     --output my_ludo_cards.png")
    
    click.echo("\n3️⃣  Using configuration file:")
    click.echo("   python png_mixer_cli.py batch \\")
    click.echo("     --config my_settings.json \\")
    click.echo("     --common a.png --uncommon b.png --legendary c.png \\")
    click.echo("     --normal xp.png --special xpxd.png")
    
    click.echo("\n4️⃣  View current configuration:")
    click.echo("   python png_mixer_cli.py config")
    
    click.echo("\n💡 Tips:")
    click.echo("   • All images must be 500x500 PNG format")
    click.echo("   • A:B ratio is always maintained at 1:1")
    click.echo("   • Output is DIN A4 format (2480x3508 pixels)")
    click.echo("   • 6 images per row")


if __name__ == '__main__':
    cli()
