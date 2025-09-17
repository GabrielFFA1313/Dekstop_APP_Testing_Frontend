# NAVIGATION_ROUTER.PY - Router-based navigation system using JSON
import json
import os
from datetime import datetime
from PyQt6.QtCore import QDate, QTime


class NavigationRouter:
    """Router class for managing view navigation and state using JSON"""
    
    def __init__(self, main_app, json_file_path="navigation_state.json"):
        self.main_app = main_app
        self.json_file_path = json_file_path
        self.current_route = None
        self.navigation_history = []
        self.view_states = {}
        self.load_navigation_state()
    
    def load_navigation_state(self):
        """Load navigation state from JSON file"""
        try:
            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # Load and deserialize current_route
                current_route_data = data.get('current_route', {
                    'view': 'calendar',
                    'params': {}
                })
                self.current_route = {
                    'view': current_route_data['view'],
                    'params': self._deserialize_view_state(current_route_data.get('params', {}))
                }
                
                # Load and deserialize navigation_history
                history_data = data.get('navigation_history', [])
                self.navigation_history = []
                for history_item in history_data:
                    deserialized_item = {
                        'view': history_item['view'],
                        'params': self._deserialize_view_state(history_item.get('params', {})),
                        'timestamp': history_item['timestamp']
                    }
                    self.navigation_history.append(deserialized_item)
                
                # Load and deserialize view_states
                states_data = data.get('view_states', {})
                self.view_states = {}
                for view, state in states_data.items():
                    self.view_states[view] = self._deserialize_view_state(state)
                
                print(f"Loaded navigation state: {self.current_route['view']}")
            else:
                # Initialize with default route
                self.current_route = {
                    'view': 'calendar',
                    'params': {}
                }
                self.navigation_history = []
                self.view_states = {}
                
        except Exception as e:
            print(f"Error loading navigation state: {e}")
            # Fallback to defaults
            self.current_route = {'view': 'calendar', 'params': {}}
            self.navigation_history = []
            self.view_states = {}
    
    def save_navigation_state(self):
        """Save navigation state to JSON file"""
        try:
            # Convert QDate and QTime objects to strings for JSON serialization
            serializable_states = {}
            for view, state in self.view_states.items():
                serializable_states[view] = self._serialize_view_state(state)
            
            # Serialize current_route params
            serialized_current_route = {
                'view': self.current_route['view'],
                'params': self._serialize_view_state(self.current_route['params'])
            }
            
            # Serialize navigation_history
            serialized_history = []
            for history_item in self.navigation_history:
                serialized_item = {
                    'view': history_item['view'],
                    'params': self._serialize_view_state(history_item['params']),
                    'timestamp': history_item['timestamp']
                }
                serialized_history.append(serialized_item)
            
            navigation_data = {
                'current_route': serialized_current_route,
                'navigation_history': serialized_history,
                'view_states': serializable_states,
                'metadata': {
                    'last_updated': datetime.now().isoformat(),
                    'app_version': '1.0'
                }
            }
            
            with open(self.json_file_path, 'w', encoding='utf-8') as file:
                json.dump(navigation_data, file, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving navigation state: {e}")
            return False
    
    def _serialize_view_state(self, state):
        """Convert PyQt objects to JSON-serializable format"""
        if not isinstance(state, dict):
            return state
            
        serialized = {}
        for key, value in state.items():
            if isinstance(value, QDate):
                serialized[key] = value.toString("yyyy-MM-dd")
            elif isinstance(value, QTime):
                serialized[key] = value.toString("hh:mm")
            elif isinstance(value, dict):
                serialized[key] = self._serialize_view_state(value)
            else:
                serialized[key] = value
        
        return serialized
    
    def _deserialize_view_state(self, state):
        """Convert JSON data back to PyQt objects"""
        if not isinstance(state, dict):
            return state
            
        deserialized = {}
        for key, value in state.items():
            if key.endswith('_date') and isinstance(value, str):
                deserialized[key] = QDate.fromString(value, "yyyy-MM-dd")
            elif key.endswith('_time') and isinstance(value, str):
                deserialized[key] = QTime.fromString(value, "hh:mm")
            elif isinstance(value, dict):
                deserialized[key] = self._deserialize_view_state(value)
            else:
                deserialized[key] = value
        
        return deserialized
    
    def navigate_to(self, view_name, params=None, save_current=True):
        """Navigate to a specific view with optional parameters"""
        if params is None:
            params = {}
        
        try:
            # Save current view state before navigating
            if save_current and self.current_route:
                self._save_current_view_state()
                
                # Add to navigation history
                self.navigation_history.append({
                    'view': self.current_route['view'],
                    'params': self.current_route['params'].copy(),
                    'timestamp': datetime.now().isoformat()
                })
                
                # Limit history size
                if len(self.navigation_history) > 50:
                    self.navigation_history = self.navigation_history[-50:]
            
            # Update current route
            self.current_route = {
                'view': view_name,
                'params': params.copy()
            }
            
            # Save navigation state
            self.save_navigation_state()
            
            # Perform the actual view switch
            self._switch_to_view(view_name, params)
            
            print(f"Navigated to: {view_name} with params: {params}")
            return True
            
        except Exception as e:
            print(f"Error navigating to {view_name}: {e}")
            return False
    
    def go_back(self):
        """Navigate back to the previous view"""
        if not self.navigation_history:
            print("No navigation history available")
            return False
        
        try:
            # Get the last route from history
            previous_route = self.navigation_history.pop()
            
            # Navigate without adding to history (to avoid loop)
            return self.navigate_to(
                previous_route['view'],
                previous_route['params'],
                save_current=False
            )
            
        except Exception as e:
            print(f"Error going back: {e}")
            return False
    
    def get_navigation_history(self):
        """Get the navigation history"""
        return self.navigation_history.copy()
    
    def clear_history(self):
        """Clear navigation history"""
        self.navigation_history = []
        self.save_navigation_state()
    
    def _save_current_view_state(self):
        """Save the current view's state"""
        current_view = self.current_route['view']
        
        # Collect view-specific state
        view_state = {}
        
        if current_view == 'calendar':
            view_state = self._get_calendar_state()
        elif current_view == 'day_view':
            view_state = self._get_day_view_state()
        elif current_view == 'activities':
            view_state = self._get_activities_state()
        elif current_view == 'add_event' or current_view == 'edit_event':
            view_state = self._get_event_form_state()
        
        # Store in view_states
        self.view_states[current_view] = view_state
    
    def _get_calendar_state(self):
        """Get calendar view state"""
        state = {}
        if hasattr(self.main_app, 'calendar_ui') and self.main_app.calendar_ui:
            if hasattr(self.main_app.calendar_ui, 'calendarWidget'):
                state['selected_date'] = self.main_app.calendar_ui.calendarWidget.selectedDate()
            if hasattr(self.main_app.calendar_ui, 'comboUpcomingFilter'):
                state['filter_selection'] = self.main_app.calendar_ui.comboUpcomingFilter.currentText()
        return state
    
    def _get_day_view_state(self):
        """Get day view state"""
        state = {}
        if hasattr(self.main_app, 'current_date'):
            state['current_date'] = self.main_app.current_date
        if hasattr(self.main_app, 'day_view_manager') and self.main_app.day_view_manager.day_view_ui:
            if hasattr(self.main_app.day_view_manager.day_view_ui, 'comboUpcomingFilter'):
                state['filter_selection'] = self.main_app.day_view_manager.day_view_ui.comboUpcomingFilter.currentText()
        return state
    
    def _get_activities_state(self):
        """Get activities view state"""
        state = {}
        if hasattr(self.main_app, 'activities_manager') and self.main_app.activities_manager.activities_ui:
            if hasattr(self.main_app.activities_manager.activities_ui, 'comboActivityType'):
                state['activity_filter'] = self.main_app.activities_manager.activities_ui.comboActivityType.currentText()
            if hasattr(self.main_app.activities_manager.activities_ui, 'comboUpcomingFilter'):
                state['upcoming_filter'] = self.main_app.activities_manager.activities_ui.comboUpcomingFilter.currentText()
        return state
    
    def _get_event_form_state(self):
        """Get event form state"""
        state = {}
        # We typically don't want to save form data for security/privacy reasons
        # But we can save form metadata
        if hasattr(self.main_app, 'add_event_manager'):
            state['mode'] = getattr(self.main_app.add_event_manager, 'mode', 'add')
        return state
    
    def _switch_to_view(self, view_name, params):
        """Actually switch to the specified view"""
        # Clear current central widget
        self.main_app.setCentralWidget(None)
        
        # Force garbage collection
        import gc
        gc.collect()
        
        # Restore view state if available
        saved_state = self.view_states.get(view_name, {})
        if saved_state:
            saved_state = self._deserialize_view_state(saved_state)
        
        # Switch to the appropriate view using main app's create methods
        if view_name == 'calendar':
            self.main_app.create_calendar_view(params, saved_state)
        elif view_name == 'day_view':
            self.main_app.create_day_view(params, saved_state)
        elif view_name == 'activities':
            self.main_app.create_activities_view(params, saved_state)
        elif view_name == 'add_event':
            self.main_app.create_add_event_view(params, saved_state)
        elif view_name == 'edit_event':
            self.main_app.create_edit_event_view(params, saved_state)
        elif view_name == 'search':
            self.main_app.create_search_view(params, saved_state)
        else:
            raise ValueError(f"Unknown view: {view_name}")
    
    def _setup_calendar_view(self, params, saved_state):
        """Setup calendar view with state restoration (REMOVED - use main app method)"""
        pass
    
    def _setup_day_view(self, params, saved_state):
        """Setup day view with state restoration (REMOVED - use main app method)"""
        pass
    
    def _setup_activities_view(self, params, saved_state):
        """Setup activities view with state restoration (REMOVED - use main app method)"""
        pass
    
    def _setup_add_event_view(self, params, saved_state):
        """Setup add event view (REMOVED - use main app method)"""
        pass
    
    def _setup_edit_event_view(self, params, saved_state):
        """Setup edit event view (REMOVED - use main app method)"""
        pass
    
    def _setup_search_view(self, params, saved_state):
        """Setup search view (REMOVED - use main app method)"""
        pass
    
    # Convenience methods for common navigation patterns
    def to_calendar(self, selected_date=None):
        """Navigate to calendar view"""
        params = {}
        if selected_date:
            params['selected_date'] = selected_date
        return self.navigate_to('calendar', params)
    
    def to_day_view(self, date=None):
        """Navigate to day view"""
        params = {}
        if date:
            params['date'] = date
        return self.navigate_to('day_view', params)
    
    def to_activities(self):
        """Navigate to activities view"""
        return self.navigate_to('activities')
    
    def to_add_event(self):
        """Navigate to add event view"""
        return self.navigate_to('add_event')
    
    def to_edit_event(self, event_data):
        """Navigate to edit event view"""
        return self.navigate_to('edit_event', {'event_data': event_data})
    
    def to_search(self, query=''):
        """Navigate to search view"""
        return self.navigate_to('search', {'query': query})
    
    def get_current_route(self):
        """Get the current route information"""
        return self.current_route.copy()
    
    def is_current_view(self, view_name):
        """Check if the specified view is currently active"""
        return self.current_route['view'] == view_name