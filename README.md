# ModFax

ModFax is a Python project that utilizes Poetry and Praw to provide a streamlined way of broadcasting messages to all moderators of a subreddit.

## Installation

1. `poetry install`

## Configuration

1. `cp config.example.py config.py`
2. Fill in the necessary fields in `config.py`

## Usage

1. `poetry run python main.py`

## How To Use

1. Make sure you and the bot are both moderators of the subreddit you want to broadcast to.
2. Write a private message to the bot with the subreddit as the subject (e.g. `testsubreddit`) and the message being the message you want to broadcast, including Markdown.
3. The bot will then broadcast the message to all moderators of the subreddit.

## License

This work is under the [European Union Public License v1.2](LICENSE) or – as soon they will be approved by the European Commission - subsequent versions of the EUPL (the "Licence");

You may get a copy of this license in your language from the European Commission [here](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).

Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the Licence for the specific language governing permissions and limitations under the Licence.