import  { Schema, model, models } from 'mongoose';

const PostSchema = new Schema({
    creator: {
        type: Schema.Types.ObjectId,
        ref: 'User',        
    },
    summary: {
       type: String,
       required: [ true, 'Summary is required.'],
    },
    tag: {
        type: String,
        required: [true, 'tag is required.'], 
     }
});

const Post = models.Post || model('Post', PostSchema);

export default Post;