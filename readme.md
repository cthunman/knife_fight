# Knife Fight Card Game Analysis Engine

## Description

This is an attempt to build an analysis engine for experimenting with different card types to help balance a card game I'm working on.

## What am I trying to answer?

- What is the set of possible outcomes given two sets of cards?
- Which cards work well together?
- Are there certain classes of cards that dominate others?
    - Can I create some cyclical domination patterns? eg. A > B, B > C, C > A ??
- How do I think about the order that cards are played, and how can I reason about this element?

## Ideas for types of cards:
- Attack - Do damage immediately
- Block - Build up block level that will diminish attack effectiveness
- Parry - Completely block an opponent attack but only if the attack came immediately before this card.

- Maybe there is a concept of card classes... effects that linger, effects that are immediate, effects that change other effects.

## Different classes of player?
- Players with different default damage output
- Different sets of cards for different players?
- This might help with balance a bit... if I can create 5-6 different player classes that are different enough, even if 1 or 2 are
kind of dominant, it may be less of a big deal.

## Structure of a Game Object

Games have players
Players have cards
Cards have effects
Effects change the state of the game

## Usage

To use the `main.py` file, execute the following command:

python main.py
