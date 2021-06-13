//
//  APXCloseWindowPlugin.m
//  Close Window
//
//  Copyright 2021 Florian Pircher
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.

#import "APXCloseWindowPlugin.h"

@implementation APXCloseWindowPlugin

static NSInteger kFileMenuItemIndex = 1;
static NSInteger kViewMenuItemIndex = 6;

- (NSUInteger)interfaceVersion {
    return 1;
}

- (void)loadPlugin {
    NSBundle *pluginBundle = [NSBundle bundleForClass:APXCloseWindowPlugin.class];
    NSMenuItem *closeWindowMenuItem = [NSMenuItem new];
    closeWindowMenuItem.title = [pluginBundle localizedStringForKey:@"Close Window" value:nil table:nil];
    closeWindowMenuItem.target = self;
    closeWindowMenuItem.action = @selector(closeWindow:);
    
    NSUserDefaults *defaults = NSUserDefaults.standardUserDefaults;
    BOOL retainKeyboardEquivalent = [defaults boolForKey:kRetainKeyboardEquivalent];
    
    NSMenu *mainMenu = [NSApp mainMenu];
    
    if (!retainKeyboardEquivalent) {
        NSMenuItem *viewMenuItem = [mainMenu itemAtIndex:kViewMenuItemIndex];
        NSMenu *viewMenu = viewMenuItem.submenu;
        NSInteger conflictingMenuItemIndex = [viewMenu indexOfItemWithTarget:nil andAction:NSSelectorFromString(@"closeEditPage:")];
        
        if (conflictingMenuItemIndex != -1) {
            NSMenuItem *conflictingMenuItem = [viewMenu itemAtIndex:conflictingMenuItemIndex];
            conflictingMenuItem.keyEquivalent = @"";
            conflictingMenuItem.keyEquivalentModifierMask = 0;
        }
        
        closeWindowMenuItem.keyEquivalent = @"W";
        closeWindowMenuItem.keyEquivalentModifierMask = NSEventModifierFlagCommand | NSEventModifierFlagShift;
    }
    
    NSMenuItem *fileMenuItem = [mainMenu itemAtIndex:kFileMenuItemIndex];
    NSMenu *fileMenu = fileMenuItem.submenu;
    NSInteger closeMenuItemIndex = [fileMenu indexOfItemWithTarget:nil andAction:NSSelectorFromString(@"performClose:")];
    
    if (closeMenuItemIndex != -1) {
        [fileMenu insertItem:closeWindowMenuItem atIndex:closeMenuItemIndex + 1];
    }
    else {
        [fileMenu addItem:closeWindowMenuItem];
    }
}

- (GSDocument *)currentDocument {
    return [(GSApplication *)NSApp currentFontDocument];
}

- (void)closeWindow:(id)sender {
    [self.currentDocument close];
}

- (BOOL)validateMenuItem:(NSMenuItem *)menuItem {
    return self.currentDocument != nil;
}

@end
