package ca.mohamedmoussa.mhacks;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.AttributeSet;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import com.firebase.client.DataSnapshot;
import com.firebase.client.Firebase;
import com.firebase.client.FirebaseError;
import com.firebase.client.ValueEventListener;

public class DetailActivity extends Activity {

    String message = "";
    TextView title;
    EditText editText;
    Firebase myFirebaseRef;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Intent intent = getIntent();
        String gesture = intent.getStringExtra(MainActivity.EXTRA_MESSAGE);

        switch (gesture) {
            case "Circle":
                message = "circleMessage";
                break;
            case "Swipe":
                message = "swipeMessage";
                break;
            case "Key Tap":
                message = "keyTapMessage";
                break;
            case "Screen Tap":
                message = "screenTapMessage";
                break;
            case "Number One":
                message = "numberOneMessage";
                break;
            case "Gun":
                message = "gunMessage";
                break;
            case "Stop":
                message = "stopMessage";
                break;
        }

        setContentView(R.layout.activity_detail);

        title = (TextView) findViewById(R.id.title);
        editText = (EditText) findViewById(R.id.editText);
        title.setText(gesture);

        Firebase.setAndroidContext(this);
        myFirebaseRef = new Firebase("https://MYLINK.firebaseio.com/");
        myFirebaseRef.child(message).addValueEventListener(new ValueEventListener() {

            @Override
            public void onDataChange(DataSnapshot snapshot) {
                editText.setText(snapshot.getValue().toString());
            }

            @Override
            public void onCancelled(FirebaseError error) {
                System.out.println(error.getMessage());
            }

        });

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_detail, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void exit(View view) {
        myFirebaseRef.child(message).setValue(editText.getText().toString());
        finish();
    }
}
